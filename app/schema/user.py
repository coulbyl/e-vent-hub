from ma import ma


class UserSchema(ma.Schema):
    class Meta:
        fields = (
            '_id',
            'firstname',
            'lastname',
            'email',
            'contacts',
            'photo',
            # 'favourite_events',
            'active',
            'created_at',
            'updated_at'
        )
    #favourite_events = ma.Nested(EventSchema, many=True)
