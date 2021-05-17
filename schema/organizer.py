from ma import ma


class OrganizerSchema(ma.Schema):
    class Meta:
        fields = (
            '_id',
            'name',
            'contacts',
            'email',
            'photo',
            'active',
            # 'events',
            'created_at',
            'updated_at'
        )

        #events = ma.Nested(EventSchema, many=True)
