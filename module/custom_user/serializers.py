from rest_framework import serializers
from datetime import datetime, timedelta

from .models import CustomUser
from module.hall.models import Address

# register
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(required=True, write_only=True)
    phone_number = serializers.CharField(min_length=10, max_length=15)
    stripe_customer_id = serializers.CharField(required=False)
    # def to_representation(self, instance):
    #     # Customizing the representation of the instance
    #     representation = super().to_representation(instance)
    #     representation['custom_field'] = 'Custom value'
    #     return representation

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "password",
            "confirm_password",
            "email",
            "phone_number",
            "dob",
            "stripe_customer_id",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def validate_email(self, attrs):
        if CustomUser.objects.filter(email=attrs):
            raise serializers.ValidationError("Email already exists.")
        return attrs
    
    def validate_phone_number(self, attrs):
        if not attrs.isdigit() or len(attrs) < 10 or len(attrs) > 15:
            raise serializers.ValidationError("Invalid phone number.")
        
        if CustomUser.objects.filter(phone_number=attrs):
            raise serializers.ValidationError("Phone number already exists.")
        return attrs
        
    def validate_dob(self, attrs):
        current_date = datetime.now().date()
        if attrs > current_date:
            raise serializers.ValidationError("Date cannot be in the future")
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        print(validated_data)

        stripe_customer_id = validated_data.pop('stripe_customer_id', None)
        customer = CustomUser.objects.create_user(**validated_data)
        if stripe_customer_id:
            customer.stripe_customer_id = stripe_customer_id
            customer.save()
        return customer


# login
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=8)

    # class Meta:
    #     model = CustomUser
    #     fields = [
    #         "username",
    #         "password",
    #     ]

    # def to_representation(self, instance):
    #     # Customizing the representation of the instance
    #     representation = super().to_representation(instance)
    #     representation['custom_field'] = 'Custom value'
    #     return representation

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = CustomUser.objects.filter(username=username).first()

        if user and user.check_password(password):
            attrs["user"] = user
            return attrs
        else:
            raise serializers.ValidationError(
                "Unable to log in with provided credentials."
            )

# get profile
class ProfileSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(required=False)
    # email = serializers.CharField(required=False)
    # phone_number = serializers.CharField(required=False)
    # dob = serializers.DateField(required=False)
    # avatar = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = (
            "id", 
            "username", 
            "email", 
            "phone_number", 
            "dob", 
            "avatar", 
            "avatar_name", 
            "stripe_customer_id", 
            "stripe_pm_id", 
            "stripe_account_id", 
            "address_id"
        )

    def validate_email(self, attrs):
        if CustomUser.objects.filter(email=attrs):
            raise serializers.ValidationError("Email already exists")
        return attrs
    
    def validate_phone_number(self, attrs):
        if not attrs.isdigit() or len(attrs) < 10 or len(attrs) > 15:
            raise serializers.ValidationError("Invalid phone number")
        
        if CustomUser.objects.filter(phone_number=attrs):
            raise serializers.ValidationError("Phone number already exists")
        return attrs
        
    def validate_dob(self, attrs):
        current_date = datetime.now().date()
        if attrs > current_date:
            raise serializers.ValidationError("Date cannot be in the future")
        return attrs
    
    def validate_address_id(self, attrs):
        if not Address.objects.filter(id=attrs):
            raise serializers.ValidationError("Address doesn't exist")
        return attrs
    
    def update(self, instance, validated_data):      
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.dob = validated_data.get('dob', instance.dob)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.avatar_name = validated_data.get('avatar_name', instance.avatar_name)
        instance.address_id = validated_data.get('address_id', instance.address_id)
        instance.stripe_account_id = validated_data.get('stripe_account_id', instance.stripe_account_id)
        instance.stripe_pm_id = validated_data.get('stripe_pm_id', instance.stripe_pm_id)

        instance.save()
        return instance



