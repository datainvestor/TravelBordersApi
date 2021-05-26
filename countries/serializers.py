from rest_framework import serializers

from .models import Country, OriginCountry, BorderStatus

class BorderStatusSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField(source='destination.id')
    name = serializers.ReadOnlyField(source='destination.name')

    class Meta:
        model = BorderStatus
        fields = ('id', 'name', 'status')

class OriginCountrySerializer(serializers.ModelSerializer):
    origin_country = serializers.StringRelatedField(read_only=True)
    destinations = serializers.StringRelatedField(many=True, read_only=True)
    dest_country = serializers.SerializerMethodField()


    #allow new param that filters by status inside the borderstatusset
    def get_dest_country(self, instance):
        qs = instance.borderstatus_set.all()
        request = self.context["request"]
        value = request.query_params.get("my_country_param")
        if value:
            qs = instance.borderstatus_set.filter(status=value)
        return BorderStatusSerializer(qs, many=True).data

    class Meta:
        model = OriginCountry
        fields = ('origin_country', 'destinations', 'dest_country')



class BorderStatusEditorSerializer(serializers.ModelSerializer):
    """Create serializer for editing single connection based on origin and destination name- to change status"""

    #with primarykeyrelatedfield (orw without anything) it works properly but returns pks instead of names
    # origin_country = serializers.PrimaryKeyRelatedField(queryset=OriginCountry.objects.all(), read_only=False)
    # destination = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), read_only=False)
    # print(OriginCountry.objects.all())
    #
    # print("anotherone", Country.objects.all())
    origin_country = serializers.SlugRelatedField(queryset=OriginCountry.objects.all(), slug_field='origin_country_name')
    destination = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field='name')

    class Meta:
        model = BorderStatus
        fields = ('id','origin_country', 'destination', 'status')

    def create(self, validated_data):
        print(validated_data)
        customer_serializer = OriginCountrySerializer(validated_data.pop('origin_country', []))
        customer_serializer.save()
        return BorderStatus.objects.create(**validated_data)

class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('name',)

    def to_representation(self, instance):
        data = super(CountrySerializer, self).to_representation(instance)
        x = {}
        for ix,item in data.items():
            x["name"]=item
            x["color"]="blue"
        return x
