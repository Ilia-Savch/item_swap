from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ads.models import Ad, Category, ExchangeProposal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name',]

# Ad


class AdCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "description",
            "image_url",
            "category",
            "condition",
            "user",
        )

    def create(self, validated_data):
        return super().create(validated_data)


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "description",
            "image_url",
            "category",
            "condition",
        )


class AdListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Ad
        fields = (
            "id",
            "title",
            "user",
            "description",
            "image_url",
            "category",
            "condition",
            "created_at",
        )

# ExchangeProposal


class ExchangeProposalCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeProposal

        fields = (
            "ad_sender",
            "ad_receiver",
            "comment",
        )

    def validate(self, attrs):
        cur_user = self.context["request"].user
        my_ads = Ad.objects.filter(user=cur_user)
        ad_sender = attrs["ad_sender"]
        ad_receiver = attrs["ad_receiver"]

        if attrs["ad_sender"] not in my_ads:
            raise ValidationError(
                {"ad_sender": "Вы можете отправлять предложения только от своих объявлений."})

        if attrs["ad_receiver"] in my_ads:
            raise ValidationError(
                {"ad_receiver": "Нельзя отправлять предложение самому себе."})

        if ExchangeProposal.objects.filter(ad_receiver=ad_receiver, ad_sender=ad_sender).exists():
            raise ValidationError({"error": "Данный обмен уже существует"})

        return super().validate(attrs)


class ExchangeProposalUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeProposal

        fields = (
            "status",
        )


class ExchangeProposalListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExchangeProposal

        fields = (
            "ad_sender",
            "ad_receiver_id",
            "comment",
            "status",
        )
