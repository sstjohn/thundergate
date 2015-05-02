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

#ifndef _STATS_H_
#define _STATS_H_

struct mac_stats_regs {
    u32 ifHCOutOctets;
    u32 ofs_04;
    u32 etherStatsCollisions;
    u32 outXonSent;

    u32 outXoffSent;
    u32 ofs_14;
    u32 dot3StatsInternalMacTransmitErrors;
    u32 dot3StatsSingleCollisionFrames;

    u32 dot3StatsMultipleCollisionFrames;
    u32 dot3StatsDeferredTransmissions;
    u32 ofs_28;
    u32 dot3StatsExcessiveTransmissions;
    
    u32 dot3StatsLateCollisions;
    u32 ofs_34;
    u32 ofs_38;
    u32 ofs_3c;
    
    u32 ofs_40;
    u32 ofs_44;
    u32 ofs_48;
    u32 ofs_4c;
    
    u32 ofs_50;
    u32 ofs_54;
    u32 ofs_58;
    u32 ofs_5c;
    
    u32 ofs_60;
    u32 ofs_64;
    u32 ofs_68;
    u32 iHCOutUcastPkts;

    u32 iHCOutMulticastPkts;
    u32 iHCOutBroadcastPkts;
    u32 ofs_78;
    u32 ofs_7c;

    u32 iHCOOutOctets;
    u32 ofs_84;
    u32 etherStatsFragments;
    u32 ifHCInUcastPkts;

    u32 ifHCInMulticastPkts;
    u32 ifHCInBroadcastPkts;
    u32 dot3StatsFCSErrors;
    u32 dot3StatsAlignmentErrors;

    u32 xonPauseFrameReceived;
    u32 xoffPauseFrameReceived;
    u32 macControlFramesReceived;
    u32 xoffStateEntered;

    u32 dot3StatsFramesTooLongs;
    u32 etherStatsJabbers;
    u32 etherStatsUndersizePkts;
    u32 ofs_bc;
};

#endif
