# walkease/store/migrations/0006_add_missing_description_manual.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_merge_20250614_0119'),  # Adjust this to your latest migration file's name
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            ALTER TABLE store_product
            ADD COLUMN description text;
            """,
            reverse_sql="""
            ALTER TABLE store_product
            DROP COLUMN description;
            """,
        ),
    ]