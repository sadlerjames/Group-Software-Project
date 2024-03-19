�
    ���e0  �                   ��   � d Z ddlmZ ddlmZmZ ddlmZ ddlT  edej        d�	�  �         ed
ej	        d�	�  �         edej        d�	�  �         edej
        d�	�  �        gZdS )a}  
URL configuration for EcoExe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
�    )�admin)�path�include�   )�views)�*� �	dashboard)�namezlogin/�loginz
dashboard/zquiz/create/�createN)�__doc__�django.contribr   �django.urlsr   r   r	   r   r
   �
login_view�creation_view�urlpatterns� �    �?C:\Users\djhar\Documents\Projects\gsp\EcoExe\gamekeeper\urls.py�<module>r      s�   ��� �  !�  �  �  �  �  � %� %� %� %� %� %� %� %� � � � � � � � � � � 	�D��U�_�K�0�0�0��D��5�#�7�3�3�3��D��u��[�9�9�9��D���,�8�<�<�<�	���r   