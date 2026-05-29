from rest_framework import serializers
from .models import Project, Membership, Favorite


class ListingSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)
    participant_count = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at')

    def get_participant_count(self, obj):
        return obj.participants.count()

    def get_is_favorited(self, obj):
        u = self.context.get('request')
        if u and u.user.is_authenticated:
            return obj.favorited_by.filter(user=u.user).exists()
        return False


class MembershipSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.ImageField(source='user.avatar', read_only=True)

    class Meta:
        model = Membership
        fields = '__all__'
        read_only_fields = ('created_at',)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        read_only_fields = ('created_at',)
