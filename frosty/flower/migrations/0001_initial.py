# Generated by Django 2.2.16 on 2022-07-31 09:52

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('customer', '????????????????????'), ('seller', '????????????????')], default='customer', max_length=8, verbose_name='????????')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='?????????????? ?????????? ??????????????????????', verbose_name='?????????? ??????????????????????')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='???????? ????????????????')),
            ],
            options={
                'verbose_name': '?????????????????????? ?? ????????????',
                'verbose_name_plural': '?????????????????????? ?? ????????????',
            },
        ),
        migrations.CreateModel(
            name='Flower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='????????????????')),
                ('colour', models.CharField(choices=[('white', '??????????'), ('red', '??????????????'), ('orange', '??????????????????'), ('yellow', '????????????'), ('green', '??????????????'), ('blue', '??????????/??????????????'), ('violet', '????????????????????'), ('pink', '??????????????'), ('black', '????????????')], default='white', max_length=6, verbose_name='????????')),
            ],
            options={
                'verbose_name': '????????????',
                'verbose_name_plural': '??????????',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='????????????????????')),
                ('price', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='????????')),
                ('visible', models.BooleanField(default=True, verbose_name='?????????????????????')),
                ('flower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='flower.Flower', verbose_name='??????????')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to=settings.AUTH_USER_MODEL, verbose_name='????????????????')),
            ],
            options={
                'verbose_name': '??????',
                'verbose_name_plural': '????????',
                'ordering': ['seller', 'flower'],
            },
        ),
        migrations.AddConstraint(
            model_name='flower',
            constraint=models.UniqueConstraint(fields=('name', 'colour'), name='unique_name_colour'),
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='??????????'),
        ),
        migrations.AddField(
            model_name='comment',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='flower.Item', verbose_name='??????????'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddConstraint(
            model_name='item',
            constraint=models.UniqueConstraint(fields=('seller', 'flower'), name='unique_seller_flower'),
        ),
    ]
