from rest_framework import serializers

class PostSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(allow_blank=True, required=False)
    urn = serializers.CharField(allow_blank=True, required=False)
    person = serializers.SerializerMethodField()
    postedAt = serializers.DateTimeField()

    def get_person(self, obj):
        person_data = obj.get('person', {})  # Manejar el caso cuando no se proporciona información de la persona
        return {
            'name': person_data.get('name', ''),
            'description': person_data.get('description', ''),
            'link': person_data.get('link', ''),
        }