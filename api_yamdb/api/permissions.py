from rest_framework import permissions


class IsModeratorAdminAuthorOrReadOnly(permissions.BasePermission):
    '''
    Действия допустимые для  суперпользавтеля, админа,
    модератора, автора и анонима.
    '''
    def has_permission(self, request, view):
        '''Допускаемые типы запросов.'''
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        '''Определяем допустимые действия с объектом.'''
        if request.method == 'POST':
            return request.user.is_authenticated

        # Изменить пост может только автор, админ и суперпользавтель.
        if request.method in ('PUT', 'PATCH'):
            return (
                request.user.is_admin
                or obj.author == request.user
            )

        # Удалить пост может автор, модератор, админ и суперпользавтель.
        if request.method == 'DELETE':
            return (
                request.user.is_moderator
                or request.user.is_admin
                or obj.author == request.user
            )


class IsAdminOrReadOnly(permissions.BasePermission):
    '''Разрешено только админу остальным только чтение.'''
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAdmin(permissions.BasePermission):
    '''Разрешно только админу.'''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class PermissionsForReviewsAndComments(permissions.BasePermission):
    '''
    Допустимые действия с отзывами / комментариями
    для  суперпользавтеля, админа, модератора, автора и анонима.
    '''
    def has_permission(self, request, view):
        '''Допускаемые типы запросов.'''
        # Анониму доступен запрос списка отзывов / комментариев
        # или один отзыв / комментарий.
        # Для всех иных действий - требуется аутентификация.
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        '''Определяем допустимые действия с объектом.'''
        # Любой аутентифицированный пользователь может
        # разместить отзыв / комментарий.
        if request.method == 'POST':
            return request.user.is_authenticated

        # Изменить или удалить отзыв / комментарий может только его автор,
        # админ, суперпользавтель или модератор.
        elif request.method in ('PUT', 'PATCH', 'DELETE'):
            return (
                request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user
            )
        # Для 'GET', 'HEAD', 'OPTIONS' аутентификация не требуется.
        else:
            return True
