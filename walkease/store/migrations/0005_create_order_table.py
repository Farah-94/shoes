from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_order_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipping_address', models.TextField()),
                ('payment_method', models.CharField(max_length=50)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.00, max_digits=10)),
                ('status', models.CharField(default='Processing', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(to='store.OrderItem')),
            ],
        ),
    ]
