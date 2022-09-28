from django.db import models


class Orders(models.Model):
    table_row_index = models.IntegerField(unique=True)
    table_row_number = models.IntegerField()
    order_number = models.IntegerField(
        unique=True,
        verbose_name='Номер заказа'
    )
    cost_usd = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена в долларах'
    )
    cost_rub = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Цена в рубля'
    )
    delivery_date = models.CharField(
        max_length=10,
        verbose_name='Дата доставки'
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        verbose_name='Дата обновления'
    )

    class Meta:
        managed = False
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.order_number
