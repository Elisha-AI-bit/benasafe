# Generated manually to fix role field null constraint

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_add_role_and_bouquet_fields'),
    ]

    operations = [
        # Use raw SQL to modify the existing table since it wasn't created through migrations
        migrations.RunSQL(
            # SQLite query to check and modify the role_id column to allow NULL
            """
            PRAGMA foreign_keys=OFF;
            CREATE TABLE IF NOT EXISTS accounts_userprofile_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                phone VARCHAR(20) DEFAULT '',
                nrc VARCHAR(20) DEFAULT '',
                date_of_birth DATE,
                address TEXT DEFAULT '',
                profile_picture VARCHAR(100),
                is_email_verified BOOLEAN NOT NULL DEFAULT 0,
                subscription_active BOOLEAN NOT NULL DEFAULT 1,
                subscription_start_date DATE NOT NULL,
                subscription_end_date DATE,
                verification_status VARCHAR(20) NOT NULL DEFAULT 'pending',
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                bouquet_id INTEGER,
                role_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
                FOREIGN KEY (bouquet_id) REFERENCES accounts_bouquet(id) ON DELETE RESTRICT,
                FOREIGN KEY (role_id) REFERENCES accounts_userrole(id) ON DELETE RESTRICT
            );
            INSERT INTO accounts_userprofile_new (
                id, user_id, phone, nrc, date_of_birth, address, profile_picture,
                is_email_verified, subscription_active, subscription_start_date,
                subscription_end_date, verification_status, created_at, updated_at,
                bouquet_id, role_id
            )
            SELECT id, user_id, phone, nrc, date_of_birth, address, profile_picture,
                   is_email_verified, subscription_active, subscription_start_date,
                   subscription_end_date, verification_status, created_at, updated_at,
                   bouquet_id, role_id
            FROM accounts_userprofile;
            DROP TABLE accounts_userprofile;
            ALTER TABLE accounts_userprofile_new RENAME TO accounts_userprofile;
            PRAGMA foreign_keys=ON;
            """,
            reverse_sql="""
            PRAGMA foreign_keys=OFF;
            -- Reverse is complex, so we'll just ensure the constraints are properly set
            PRAGMA foreign_keys=ON;
            """
        ),
    ]
