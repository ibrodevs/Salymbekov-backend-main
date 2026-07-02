from django.db import migrations


GALLERY_IMAGES = [
    {
        "id": 1,
        "url": "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2745.jpg",
        "title": "Material and technical base",
        "category": "Infrastructure",
    },
    {
        "id": 2,
        "url": "https://salymbekov.com/wp-content/uploads/2021/03/c0b9392.jpg",
        "title": "Modern laboratories",
        "category": "Science",
    },
    {
        "id": 3,
        "url": "https://salymbekov.com/wp-content/uploads/2021/03/c0b9391.jpg",
        "title": "Educational spaces",
        "category": "Education",
    },
    {
        "id": 4,
        "url": "https://salymbekov.com/wp-content/uploads/2021/03/c0b9389.jpg",
        "title": "Clinical base",
        "category": "Medicine",
    },
    {
        "id": 5,
        "url": "https://salymbekov.com/wp-content/uploads/2021/03/c0b9390.jpg",
        "title": "Technology equipment",
        "category": "Technology",
    },
    {
        "id": 6,
        "url": "https://salymbekov.com/wp-content/uploads/2022/07/photo_2022-07-18_15-21-07.jpg",
        "title": "Innovation solutions",
        "category": "Development",
    },
    {
        "id": 7,
        "url": "https://salymbekov.com/wp-content/uploads/2022/07/bc0b2562.jpg",
        "title": "Quality resources",
        "category": "Resources",
    },
]


def seed_content(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")

    PageContent.objects.update_or_create(
        slug="home-video",
        defaults={
            "title_en": "University Video",
            "data": {
                "platform": "YouTube",
                "youtube_id": "SdluvCyzd6M",
            },
            "is_active": True,
        },
    )

    PageContent.objects.update_or_create(
        slug="material-base-gallery",
        defaults={
            "title_en": "Material and Technical Base",
            "data": {
                "images": GALLERY_IMAGES,
            },
            "is_active": True,
        },
    )


def remove_seed_content(apps, schema_editor):
    PageContent = apps.get_model("about", "PageContent")
    PageContent.objects.filter(slug__in=["home-video", "material-base-gallery"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("about", "0004_pagecontent_pagemedia"),
    ]

    operations = [
        migrations.RunPython(seed_content, remove_seed_content),
    ]
