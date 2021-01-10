from rest_framework import serializers
from api.models import User, UserProfile
from  Alt.models import Shirt, Atrocity, NonProfit, Category, Rating






class CategorySerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Category
        fields=['name', 'image','information',]
        depth = 2



class AtrocitySerializer(serializers.ModelSerializer):

    category=CategorySerializer(many=True, read_only=True )


    class Meta:
        model = Atrocity
        fields = ['title', 'region', 'info', 'image_url', 'category','country','slug', 'videoURL' ]
        depth = 3




class ShirtSerializer(serializers.ModelSerializer):
    Atrocity = AtrocitySerializer(many=True, read_only =True)
    category = CategorySerializer(many = True , read_only =True)
    country=serializers.StringRelatedField()
    
    

    class Meta:
        model = Shirt
        fields = ['id', 'name', 'price', 'country', 'shirt_image','Atrocity', 'category', 'slug','original_image', 'no_of_ratings', 'average_rating']

  



class NonProfitSerializer(serializers.ModelSerializer):

    category=CategorySerializer(many=True, read_only=True)
    atrocity = AtrocitySerializer(many=True, read_only=True)
    shirtList=ShirtSerializer(many=True, read_only=True)

    class Meta:
        model = NonProfit
        fields = ['name','logo', 'description', 'year_started', 'mission_statement','vision_statement','website_url','category','slug', 'atrocity', 'shirtList', 'main_image']
        depth = 2


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields= ['user', 'shirt', 'stars']


class UserProfileSerializer(serializers.ModelSerializer):

    shirt_list= ShirtSerializer(many=True, read_only=True)
    atrocity_list= AtrocitySerializer(many= True, read_only= True)
    nonProfit_list = NonProfitSerializer(many=True, read_only=True)

      
    class Meta:
        model = UserProfile
        fields = ('title', 'dob', 'address', 'country', 'city', 'zip', 'qr_code', 'shirt_list', 'atrocity_list', 'nonProfit_list' )
        depth = 3


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)
    

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password','username',  'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()

        return instance


