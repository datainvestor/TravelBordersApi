from rest_framework import serializers

from .models import Country, OriginCountry, BorderStatus

class BorderStatusSerializer(serializers.HyperlinkedModelSerializer):
    iso_code = serializers.ReadOnlyField(source='destination.iso_code')
    class Meta:
        model = BorderStatus
        fields = ('iso_code',)



class OriginCountrySerializer(serializers.ModelSerializer):
    origin_country = serializers.StringRelatedField(read_only=True)
    # destinations = serializers.StringRelatedField(many=True, read_only=True)
    dest_country = serializers.SerializerMethodField() #this goes along with the mehtod get_dest_country


    def get_dest_country(self, instance):
        """Allow new param that filters by status inside the borderstatus model"""
        qs = instance.borderstatus_set.all()
        request = self.context["request"]
        value = request.query_params.get("my_country_param")
        if value:
            qs = instance.borderstatus_set.filter(status=value)
        return BorderStatusSerializer(qs, many=True).data


    class Meta:
        model = OriginCountry
        fields = ('origin_country', 'dest_country')

    def to_representation(self, instance):
        """Return a lit of iso_odes instead a list of dicts """
        data = super(OriginCountrySerializer, self).to_representation(instance)
        x = []
        for item in data['dest_country']:
            print(data['origin_country'])
            x.append(item['iso_code'])
        return x

class BorderStatusEditorSerializer(serializers.ModelSerializer):
    """Create serializer for editing single connection based on origin and destination name- to change status"""

    #with primarykeyrelatedfield (orw without anything) it works properly but returns pks instead of names
    origin_country = serializers.PrimaryKeyRelatedField(queryset=OriginCountry.objects.all(), read_only=False)
    destination = serializers.PrimaryKeyRelatedField(queryset=Country.objects.all(), read_only=False)


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
