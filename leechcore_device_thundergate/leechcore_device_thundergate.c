/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015-2016  Saul St. John
 *
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

/*
 * LeechCore device plugin -- bridges LeechCore / MemProcFS to a
 * ThunderGate NIC. Scatter read/write are relayed over TCP to the
 * leechbridge.py daemon, which speaks ThunderGate's raw 0x88b5 protocol
 * and performs the actual host-memory DMA through the NIC's rxcpu.
 *
 *   -device thundergate://daemon=<host>:<port>[,size=<bytes>]
 *
 * Build: drop this directory into a LeechCore-plugins checkout (next to
 * leechcore_device_skeleton) and run `make`; it needs that project's
 * includes/leechcore_device.h and the leechcore runtime library.
 *
 * The plugin ABI here follows the leechcore_device_skeleton template but
 * is UNVERIFIED against a live build. If a struct field or helper name
 * differs in your leechcore_device.h (notably LcMemMap_AddRange and
 * Config.fVolatile), adjust to match -- those lines are marked below.
 */

#include <leechcore_device.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <winsock2.h>
#include <ws2tcpip.h>
typedef SOCKET tg_sock;
#define TG_BADSOCK      INVALID_SOCKET
#define tg_close_sock   closesocket
#else
#include <sys/socket.h>
#include <netinet/in.h>
#include <netinet/tcp.h>
#include <netdb.h>
#include <unistd.h>
typedef int tg_sock;
#define TG_BADSOCK      (-1)
#define tg_close_sock   close
#endif /* _WIN32 */

#define TG_OP_READ      0
#define TG_OP_WRITE     1
#define TG_OP_INFO      2
#define TG_PORT_DEFAULT "28473"
#define TG_SIZE_DEFAULT 0x200000000ULL          /* 8 GiB */

typedef struct {
    tg_sock sock;
    QWORD cbMax;
} DEVICE_CONTEXT_TG;

/* --- TCP helpers --------------------------------------------------- */

static BOOL TG_SendAll(tg_sock s, const BYTE *pb, DWORD cb)
{
    DWORD o = 0;
    while(o < cb) {
        int n = (int)send(s, (const char *)pb + o, cb - o, 0);
        if(n <= 0) { return FALSE; }
        o += (DWORD)n;
    }
    return TRUE;
}

static BOOL TG_RecvAll(tg_sock s, BYTE *pb, DWORD cb)
{
    DWORD o = 0;
    while(o < cb) {
        int n = (int)recv(s, (char *)pb + o, cb - o, 0);
        if(n <= 0) { return FALSE; }
        o += (DWORD)n;
    }
    return TRUE;
}

/* 16-byte little-endian request header (every LeechCore host is LE) */
static VOID TG_Header(BYTE *hdr, BYTE op, QWORD addr, DWORD cb)
{
    memset(hdr, 0, 16);
    hdr[0] = op;
    memcpy(hdr + 4, &addr, 8);
    memcpy(hdr + 12, &cb, 4);
}

/* --- relay primitives ---------------------------------------------- */

static BOOL TG_ReadOne(DEVICE_CONTEXT_TG *ctx, QWORD addr, DWORD cb, PBYTE pb)
{
    BYTE hdr[16], ok;
    TG_Header(hdr, TG_OP_READ, addr, cb);
    if(!TG_SendAll(ctx->sock, hdr, 16)) { return FALSE; }
    if(!TG_RecvAll(ctx->sock, &ok, 1)) { return FALSE; }
    /* the daemon always returns status + cb bytes, so the stream stays
     * framed whether the read succeeded or not */
    if(!TG_RecvAll(ctx->sock, pb, cb)) { return FALSE; }
    return ok == 1;
}

static BOOL TG_WriteOne(DEVICE_CONTEXT_TG *ctx, QWORD addr, DWORD cb, PBYTE pb)
{
    BYTE hdr[16], ok;
    TG_Header(hdr, TG_OP_WRITE, addr, cb);
    if(!TG_SendAll(ctx->sock, hdr, 16)) { return FALSE; }
    if(!TG_SendAll(ctx->sock, pb, cb)) { return FALSE; }
    if(!TG_RecvAll(ctx->sock, &ok, 1)) { return FALSE; }
    return ok == 1;
}

static QWORD TG_Info(DEVICE_CONTEXT_TG *ctx)
{
    BYTE hdr[16], ok, resp[8];
    QWORD v;
    TG_Header(hdr, TG_OP_INFO, 0, 0);
    if(!TG_SendAll(ctx->sock, hdr, 16)) { return 0; }
    if(!TG_RecvAll(ctx->sock, &ok, 1)) { return 0; }
    if(!TG_RecvAll(ctx->sock, resp, 8)) { return 0; }
    memcpy(&v, resp, 8);
    return (ok == 1) ? v : 0;
}

/* connect to "host:port"; port defaults to TG_PORT_DEFAULT */
static tg_sock TG_Connect(LPSTR szDaemon)
{
    char host[256], *colon;
    const char *port = TG_PORT_DEFAULT;
    struct addrinfo hints, *ai, *p;
    tg_sock s = TG_BADSOCK;

    if(!szDaemon || !szDaemon[0]) { return TG_BADSOCK; }
    strncpy(host, szDaemon, sizeof(host) - 1);
    host[sizeof(host) - 1] = 0;
    colon = strrchr(host, ':');
    if(colon) { *colon = 0; port = colon + 1; }

    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_UNSPEC;
    hints.ai_socktype = SOCK_STREAM;
    if(getaddrinfo(host, port, &hints, &ai)) { return TG_BADSOCK; }
    for(p = ai; p; p = p->ai_next) {
        s = socket(p->ai_family, p->ai_socktype, p->ai_protocol);
        if(s == TG_BADSOCK) { continue; }
        if(connect(s, p->ai_addr, (int)p->ai_addrlen) == 0) { break; }
        tg_close_sock(s);
        s = TG_BADSOCK;
    }
    freeaddrinfo(ai);
    if(s != TG_BADSOCK) {
        int one = 1;
        setsockopt(s, IPPROTO_TCP, TCP_NODELAY, (const char *)&one, sizeof(one));
    }
    return s;
}

/* --- LeechCore device callbacks ------------------------------------ */

VOID DeviceTG_ReadScatter(PLC_CONTEXT ctxLC, DWORD cpMEMs, PPMEM_SCATTER ppMEMs)
{
    DEVICE_CONTEXT_TG *ctx = (DEVICE_CONTEXT_TG *)ctxLC->hDevice;
    DWORD i;
    for(i = 0; i < cpMEMs; i++) {
        PMEM_SCATTER pMEM = ppMEMs[i];
        if(pMEM->f || pMEM->cb == 0) { continue; }          /* already done */
        if(pMEM->qwA == (QWORD)-1) { continue; }            /* invalid addr */
        if(pMEM->qwA > ctx->cbMax || pMEM->cb > ctx->cbMax - pMEM->qwA) { continue; }
        if(TG_ReadOne(ctx, pMEM->qwA, pMEM->cb, pMEM->pb)) {
            pMEM->f = TRUE;
        }
    }
}

VOID DeviceTG_WriteScatter(PLC_CONTEXT ctxLC, DWORD cpMEMs, PPMEM_SCATTER ppMEMs)
{
    DEVICE_CONTEXT_TG *ctx = (DEVICE_CONTEXT_TG *)ctxLC->hDevice;
    DWORD i;
    for(i = 0; i < cpMEMs; i++) {
        PMEM_SCATTER pMEM = ppMEMs[i];
        if(pMEM->cb == 0) { continue; }
        if(pMEM->qwA == (QWORD)-1) { continue; }
        if(pMEM->qwA > ctx->cbMax || pMEM->cb > ctx->cbMax - pMEM->qwA) { continue; }
        pMEM->f = TG_WriteOne(ctx, pMEM->qwA, pMEM->cb, pMEM->pb);
    }
}

VOID DeviceTG_Close(PLC_CONTEXT ctxLC)
{
    DEVICE_CONTEXT_TG *ctx = (DEVICE_CONTEXT_TG *)ctxLC->hDevice;
    if(ctx) {
        if(ctx->sock != TG_BADSOCK) { tg_close_sock(ctx->sock); }
        ctxLC->hDevice = 0;
        free(ctx);
    }
}

_Success_(return) EXPORTED_FUNCTION
BOOL LcPluginCreate(_Inout_ PLC_CONTEXT ctxLC, _Out_opt_ PPLC_CONFIG_ERRORINFO ppErr)
{
    DEVICE_CONTEXT_TG *ctx;
    QWORD cbSize;

    (void)ppErr;
    ctx = (DEVICE_CONTEXT_TG *)calloc(1, sizeof(DEVICE_CONTEXT_TG));
    if(!ctx) { return FALSE; }

#ifdef _WIN32
    { WSADATA wsa; WSAStartup(MAKEWORD(2, 2), &wsa); }
#endif
    ctx->sock = TG_Connect(LcDeviceParameterGet(ctxLC, "daemon"));
    if(ctx->sock == TG_BADSOCK) {
        lcprintf(ctxLC, "device_thundergate: cannot reach the leechbridge "
                        "daemon -- need -device thundergate://daemon=<host>:<port>\n");
        free(ctx);
        return FALSE;
    }

    /* size: explicit parameter, else ask the daemon, else default */
    cbSize = LcDeviceParameterGetNumeric(ctxLC, "size");
    if(!cbSize) { cbSize = TG_Info(ctx); }
    if(!cbSize) { cbSize = TG_SIZE_DEFAULT; }
    ctx->cbMax = cbSize;

    ctxLC->hDevice = (HANDLE)ctx;
    ctxLC->fMultiThread = FALSE;            /* the rxcpu serialises anyway */
    ctxLC->Config.fVolatile = TRUE;         /* live target, not a snapshot */
    ctxLC->pfnClose = DeviceTG_Close;
    ctxLC->pfnReadScatter = DeviceTG_ReadScatter;
    ctxLC->pfnWriteScatter = DeviceTG_WriteScatter;

    /* publish [0, cbSize) as the physical range; adjust this call to
     * your leechcore_device.h if the memory-map helper differs */
    LcMemMap_AddRange(ctxLC, 0, cbSize, 0);

    lcprintf(ctxLC, "device_thundergate: ready, %llu MiB target\n",
             (unsigned long long)(cbSize >> 20));
    return TRUE;
}
