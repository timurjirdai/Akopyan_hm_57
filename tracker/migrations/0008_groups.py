from django.db import migrations


def create_groups(apps, schema_editor):

    Group = apps.get_model(
        'auth',
        'Group'
    )


    Group.objects.create(
        name='Project Manager'
    )


    Group.objects.create(
        name='Team Lead'
    )


    Group.objects.create(
        name='Developer'
    )



class Migration(migrations.Migration):

    dependencies = [
        ('tracker','0001_initial'),
    ]


    operations = [
        migrations.RunPython(create_groups)
    ]