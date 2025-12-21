#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bene_safe.settings')
sys.path.append('c:\\Users\\THE ARCHTECT\\Documents\\projets2\\benesafe')
django.setup()

from django.db import connection

def check_userprofile_schema():
    cursor = connection.cursor()

    print("=== UserProfile Table Schema ===")
    cursor.execute("PRAGMA table_info(accounts_userprofile)")
    columns = cursor.fetchall()
    for col in columns:
        print(f"Column: {col[1]}, Type: {col[2]}, NotNull: {col[3]}, Default: {col[4]}")

    print("\n=== Foreign Key Constraints ===")
    cursor.execute("PRAGMA foreign_key_list(accounts_userprofile)")
    fkeys = cursor.fetchall()
    for fk in fkeys:
        print(f"From: {fk[2]} -> To: {fk[3]}.{fk[4]}, OnDelete: {fk[5]}")

    print("\n=== Checking for constraints ===")
    cursor.execute("PRAGMA index_list(accounts_userprofile)")
    indexes = cursor.fetchall()
    for idx in indexes:
        print(f"Index: {idx[1]}, Unique: {idx[2]}")
        cursor.execute(f"PRAGMA index_info({idx[1]})")
        info = cursor.fetchall()
        print(f"  Columns: {[col[2] for col in info]}")

if __name__ == "__main__":
    check_userprofile_schema()
