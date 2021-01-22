from rest_framework import serializers
from api.models import User, UserProfile, Balance
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
    userprofile = UserProfileSerializer(required=True)
    

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password','username',  'userprofile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **userprofile_data)
        return user

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        userprofile = instance.userprofile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        userprofile.title = userprofile_data.get('title', userprofile.title)
        userprofile.dob = userprofile_data.get('dob', userprofile.dob)
        userprofile.address = userprofile_data.get('address', userprofile.address)
        userprofile.country = userprofile_data.get('country', userprofile.country)
        userprofile.city = userprofile_data.get('city', userprofile.city)
        userprofile.zip = userprofile_data.get('zip', userprofile.zip)
        userprofile.photo = userprofile_data.get('photo', userprofile.photo)
        userprofile.save()

        return instance


