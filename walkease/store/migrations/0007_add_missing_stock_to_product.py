# walkease/store/migrations/0007_add_missing_stock_to_product.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_add_missing_description_manual'),  # adjust this to match your latest migration file name
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                ALTER TABLE store_product
                ADD COLUMN stock integer DEFAULT 0;
            """,
            reverse_sql="""
                ALTER TABLE store_product
                DROP COLUMN stock;
            """,
        ),
    ]