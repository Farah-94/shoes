from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_add_missing_stock_to_product'),  # adjust to your latest migration filename
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE store_product
                ADD COLUMN image character varying(100) NULL;
            """,
            reverse_sql="""
                ALTER TABLE store_product
                DROP COLUMN image;
            """,
        ),
    ]
