/*
 *  ThunderGate - an open source toolkit for PCI bus exploration
 *  Copyright (C) 2015  Saul St. John
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

#include "dmarf.h"

#define SPLASH_LOGO_LINES 6
#define SPLASH_TOP 10
#define SPLASH_LOGO_COLOR EFI_RED
#define SPLASH_URL_COLOR EFI_RED | EFI_BRIGHT

wchar_t *splash_logo[] = {
L"         __ __| |                     |            ___|       |",        
L"            |   __ \\  |   | __ \\   _` |  _ \\  __| |      _` | __|  _ \\", 
L"            |   | | | |   | |   | (   |  __/ |    |   | (   | |    __/", 
L"           _|  _| |_|\\__,_|_|  _|\\__,_|\\___|_|   \\____|\\__,_|\\__|\\___|" ,
L"",
L"                             http://thundergate.io"
};


#define EFI_CONSOLE_CONTROL_PROTOCOL_GUID \
	{ 0xf42f7782, 0x12e, 0x4c12, { 0x99, 0x56, 0x49, 0xf9, 0x43, 0x4, 0xf7, 0x21 } }
EFI_GUID EfiConsoleControlProtocolGuid = EFI_CONSOLE_CONTROL_PROTOCOL_GUID;

struct _EFI_CONSOLE_CONTROL_PROTOCOL;

typedef
EFI_STATUS (EFIAPI *EFI_CONSOLE_CONTROL_PROTOCOL_GET_MODE) (
		struct _EFI_CONSOLE_CONTROL_PROTOCOL *,
		int *,
		int *,  
		int *);

typedef 
EFI_STATUS (EFIAPI *EFI_CONSOLE_CONTROL_PROTOCOL_SET_MODE) (
		struct _EFI_CONSOLE_CONTROL_PROTOCOL *,
		int);

typedef
EFI_STATUS (EFIAPI *EFI_CONSOLE_CONTROL_PROTOCOL_LOCK_STD_IN) (
		struct _EFI_CONSOLE_CONTROL_PROTOCOL *,
		CHAR16 *);

typedef struct _EFI_CONSOLE_CONTROL_PROTOCOL {
	EFI_CONSOLE_CONTROL_PROTOCOL_GET_MODE GetMode;
	EFI_CONSOLE_CONTROL_PROTOCOL_SET_MODE SetMode;
	EFI_CONSOLE_CONTROL_PROTOCOL_LOCK_STD_IN LockStdIn;
} EFI_CONSOLE_CONTROL_PROTOCOL;

void splash()
{
	EFI_CONSOLE_CONTROL_PROTOCOL *cc;
	UINTN col = 0, row = 0;

	ST->ConOut->ClearScreen(ST->ConOut);

	if (EFI_SUCCESS == BS->LocateProtocol(&EfiConsoleControlProtocolGuid, 
			NULL, (void *)&cc))
	{
		int cur_mode = 0;
		cc->GetMode(cc, &cur_mode, NULL, NULL);
		if (cur_mode == 1)
			cc->SetMode(cc, 0);
	}	
	if (EFI_SUCCESS == ST->ConOut->QueryMode(ST->ConOut, 2, &col, &row)) {
		if (EFI_SUCCESS != ST->ConOut->SetMode(ST->ConOut, 2)) {
			col = 0;
			row = 0;
		}
	}
	if (0 == col || 0 == row) {
		if (EFI_SUCCESS == ST->ConOut->QueryMode(ST->ConOut, 1, &col, &row)) {
			if (EFI_SUCCESS != ST->ConOut->SetMode(ST->ConOut, 1)) {
				col = 0;
				row = 0;
			}
		}
	}
	if (0 == col || 0 == row) {
		ST->ConOut->SetMode(ST->ConOut, 0);
		col = 80;
		row = 25;
	}
	ST->ConOut->EnableCursor(ST->ConOut, 0);

	int st = (col / 2) - 40;
	ST->ConOut->SetAttribute(ST->ConOut, SPLASH_LOGO_COLOR);
	for (int ln = 0; ln < SPLASH_LOGO_LINES; ln++) {
		if (SPLASH_LOGO_LINES == ln + 1)
			ST->ConOut->SetAttribute(ST->ConOut, SPLASH_URL_COLOR);
		ST->ConOut->SetCursorPosition(ST->ConOut, st, SPLASH_TOP + ln);
		ST->ConOut->OutputString(ST->ConOut, splash_logo[ln]);
	}
	ST->ConOut->SetAttribute(ST->ConOut, EFI_WHITE);
}
