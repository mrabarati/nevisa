# Generated by Django 5.0.6 on 2024-06-02 16:44

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BlockedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('blocked', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BlockedUserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField(blank=True, null=True)),
                ('state', models.SmallIntegerField(choices=[(0, 'Unblocked'), (1, 'Blocked')], default=1)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('blocked_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='comment.blockeduser')),
                ('blocker', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.TextField()),
                ('urlhash', models.CharField(editable=False, max_length=50, unique=True)),
                ('posted', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('edited', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-posted'],
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=0)),
                ('state', models.SmallIntegerField(choices=[(1, 'Unflagged'), (2, 'Flagged'), (3, 'Flag rejected by the moderator'), (4, 'Comment modified by the author')], default=1)),
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
                ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='flags_moderated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('username', models.CharField(max_length=50)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.PositiveIntegerField(default=0)),
                ('dislikes', models.PositiveIntegerField(default=0)),
                ('comment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
            ],
        ),
        migrations.CreateModel(
            name='FlagInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.TextField(blank=True, null=True)),
                ('date_flagged', models.DateTimeField(auto_now=True)),
                ('reason', models.SmallIntegerField(choices=[(1, 'Spam | Exists only to promote a service'), (2, 'Abusive | Intended at promoting hatred'), (100, 'Something else')], default=1)),
                ('flag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to='comment.flag')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flags', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('date_flagged',),
                'unique_together': {('flag', 'user')},
            },
        ),
        migrations.CreateModel(
            name='ReactionInstance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_type', models.SmallIntegerField(choices=[(1, 'LIKE'), (2, 'DISLIKE')])),
                ('date_reacted', models.DateTimeField(auto_now=True)),
                ('reaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to='comment.reaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'reaction')},
            },
        ),
    ]
