#!/usr/bin/python3
# coding: utf-8

# original author: picoleet from the Resident Evil Modding forum
# https://residentevilmodding.boards.net/thread/15382/resident-evil-steam-save-editor

# changes:
# added --key parameter to encode mode to patch the steam id
# added update_steam_id with --key parameter to patch existing decoded save

import sys
import argparse

magic=bytes([0x00, 0x21, 0x11, 0x08, 0xC0, 0x4B, 0x00, 0x00])

def xor(data,key):
    return bytes([i^j for i,j in zip(data,key)])

def decode_savedata(in_fname, out_fname):
    global magic
    key = magic
    with open(in_fname, "rb") as fin:
        with open(out_fname, "wb") as fout:
            while (encoded_data := fin.read(8)):
                decoded_data = xor(encoded_data,key)
                fout.write(decoded_data)
                key = encoded_data

def encode_savedata(in_fname, out_fname):
    global magic
    key = magic
    with open(in_fname, "rb") as fin:
        with open(out_fname, "wb") as fout:
            while (decoded_data := fin.read(8)):
                encoded_data = xor(decoded_data,key)
                fout.write(encoded_data)
                key = encoded_data

def calculate_checksum(in_fname):
    def chksum(fin, seekpos, iters, ret):
        fin.seek(seekpos, 0)
        for i in range(iters):
            b = fin.read(4)
            val = int.from_bytes(b, byteorder='little')
            ret = (ret+val)%2**32
        return ret
    with open(in_fname, "rb") as fin:
        start1, start2 = 0x10, 0x3bb0
        len1, len2 = 0xee7, 0x5c0
        return chksum(fin, start2, len2, chksum(fin, start1, len1, 0))

def read_bytes_at_offset(in_fname, offset, count):
    with open(in_fname, "rb") as fout:
        fout.seek(offset, 0)
        return fout.read(count)

def write_bytes_at_offset(in_fname, in_bytes, offset):
    with open(in_fname, "rb+") as fout:
        fout.seek(offset, 0)
        fout.write(in_bytes)

def patch_steam_id(f, steam_id):
    source_steam_id = int.from_bytes(read_bytes_at_offset(f, 0x0, 8), byteorder='little')
    print(f"{f}: Updating Steam ID: {source_steam_id} => {steam_id}")
    write_bytes_at_offset(f, int(steam_id).to_bytes(8, byteorder='little'), 0x0)

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=["decode", "encode", "update_checksum", "show_checksum", "update_steam_id"])
    ap.add_argument('files', nargs='+', type=str)
    ap.add_argument('--key', dest="steam_id", type=str, help="Steam ID")
    args = ap.parse_args()

    if args.mode == "decode":
        for f in args.files:
            outf = "decoded_" + f
            decode_savedata(f, outf)
    elif args.mode == "encode":
        for f in args.files:
            outf = "encoded_" + f
            calc_chksum = calculate_checksum(f)
            file_chksum_bytes = read_bytes_at_offset(f, 0x8, 4)
            file_chksum = int.from_bytes(file_chksum_bytes, byteorder='little')
            if args.steam_id:
                patch_steam_id(f, args.steam_id)
            if calc_chksum != file_chksum:
                print(f"{f}: checksum mismatch detected.  Updating checksum to {hex(calc_chksum)}")
                write_bytes_at_offset(f, calc_chksum.to_bytes(4, byteorder='little'), 0x8)
            encode_savedata(f, outf)
    elif args.mode == "show_checksum":
        for f in args.files:
            chksum = calculate_checksum(f)
            print(f"{f}: {hex(chksum)}")
    elif args.mode == "update_steam_id":
        for f in args.files:
            patch_steam_id(f, args.steam_id)
    elif args.mode == "update_checksum":
        for f in args.files:
            chksum = calculate_checksum(f)
            print(f"{f}: {hex(chksum)}")
            write_bytes_at_offset(f, chksum.to_bytes(4, byteorder='little'), 0x8)
    exit(0)
