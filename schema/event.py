from ma import ma


class EventSchema(ma.Schema):
    class Meta:
        fields = (
            '_id',
            'name',
            'location',
            'description',
            'price',
            'available_places',
            'remaining_places',
            'start_at',
            'end_at',
            'image',
            'organizer_id',
            # 'participants',
            'created_at',
            'updated_at'
        )

    #participants = ma.Nested('UserSchema', many=True)
