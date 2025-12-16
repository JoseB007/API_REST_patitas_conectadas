# services/ranking_service.py
from django.db.models import Count, Q

from apps.mascotas.models import Mascota


class RankingService:

    @staticmethod
    def top_global(limit=3):
        return (
            Mascota.objects.annotate(total_likes=Count('likes'))
            .filter(total_likes__gt=0, en_adopcion=False)
            .order_by('-total_likes')[:limit]
        )

    @staticmethod
    def top_por_fecha(fecha):
        return (
            Mascota.objects.annotate(
                likes_dia=Count(
                    'likes_mascota',
                    filter=Q(likes_mascota__f_creacion__date=fecha)
                )
            )
            .filter(likes_dia__gt=0)
            .order_by('-likes_dia')
            .first()
        )

    @staticmethod
    def top_por_rango(inicio, fin):
        return (
            Mascota.objects.annotate(
                likes_rango=Count(
                    'likes_mascota',
                    filter=Q(
                        likes_mascota__f_creacion__date__range=(inicio, fin)
                    )
                )
            )
            .filter(likes_rango__gt=0)
            .order_by('-likes_rango')
            .first()
        )
