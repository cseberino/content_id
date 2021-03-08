#!/usr/bin/env python3
#
# Copyright 2021 Christian Seberino
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import hashlib
import base64

CID_ENC    = "b"
CID_VER    = b"\x01"
B32_END    = b"="
S256_CODE  = b"\x12"
S256_LEN   = b" "
DPB_ENC    = b"p"
DPB_B_SIZE = 2 ** 18
DPB_DATA   = b"\n"
DPB_LINK   = b"\x12"
D_TYPE     = b"\x08"
D_DATA     = b"\x12"
D_FL       = b"\x18"
D_BS       = b" "
L_HASH     = b"\n"
L_NAME     = b"\x12"
L_TSIZE    = b"\x18"
T_BYTES    = b"\x02"
VI_G_SIZE  = 7
BYTE       = 2
BINARY     = 2

def varint(n):
        """
        Determines varints.
        """

        bits   = bin(n)[2:]
        bits_  = "".join(reversed(bits))
        groups = [bits_[i:i + VI_G_SIZE]
                  for i in range(0, len(bits_), VI_G_SIZE)]
        groups = ["".join(reversed(e)).zfill(VI_G_SIZE) for e in groups]
        hex_   = ["1" + e for e in groups[:-1]] + ["0" + groups[-1]]
        hex_   = [hex(int(e, BINARY))[2:].zfill(BYTE) for e in hex_]
        hex_   = "".join(hex_)
        bytes_ = bytes.fromhex(hex_)

        return bytes_

def ipfs_obj(bytes_):
        """
        Creates DAG-PB encoded IPFS objects.
        """

        if len(bytes_) <= DPB_B_SIZE:
                bytes_len = varint(len(bytes_))
                data_msg  = D_TYPE + T_BYTES   +                               \
                            D_DATA + bytes_len + bytes_ +                      \
                            D_FL   + bytes_len
                ipfs_obj_ = DPB_DATA + varint(len(data_msg)) + data_msg
        else:
                data_msg  = D_TYPE + T_BYTES + D_FL + varint(len(bytes_))
                link_msgs = b""
                for e in [bytes_[i:i + DPB_B_SIZE]
                          for i in range(0, len(bytes_), DPB_B_SIZE)]:
                        mhash      = multihash(e)
                        data_msg  += D_BS    + varint(len(e))
                        link_msg   = L_HASH  + varint(len(mhash)) + mhash +   \
                                     L_NAME  + varint(0)                  +   \
                                     L_TSIZE + varint(len(ipfs_obj(e)))
                        link_msgs += DPB_LINK + varint(len(link_msg)) + link_msg
                ipfs_obj_ = link_msgs +                                        \
                            DPB_DATA  + varint(len(data_msg)) + data_msg

        return ipfs_obj_

def multihash(bytes_):
        """
        Determines multihashes of IPFS objects.
        """

        hash_ = hashlib.sha256(ipfs_obj(bytes_)).digest()

        return S256_CODE + S256_LEN + hash_

def content_id(bytes_):
        """
        Determines IPFS content identifiers.
        """

        cid = base64.b32encode(CID_VER + DPB_ENC + multihash(bytes_))
        cid = CID_ENC + cid[:cid.find(B32_END)].decode().lower()

        return cid
