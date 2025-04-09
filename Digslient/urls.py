"""
URL configuration for Digslient project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # URL สำหรับหน้า Admin
    path('admin/', admin.site.urls),
    
    # URL สำหรับแอปพลิเคชัน Paramiter พร้อม namespace
    path('', include(('Paramiter.urls', 'paramiter'), namespace='paramiter')),

    # ตัวอย่างเพิ่ม URL สำหรับ API (หากมี)
    #path('api/', include(('Paramiter.api_urls', 'api'), namespace='api')),
]

# จัดการ static และ media files ในโหมด DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# กำหนด custom error handlers (ต้องมีฟังก์ชัน custom_404 และ custom_500 ใน Paramiter.views)
handler404 = 'Paramiter.views.custom_404'
handler500 = 'Paramiter.views.custom_500'