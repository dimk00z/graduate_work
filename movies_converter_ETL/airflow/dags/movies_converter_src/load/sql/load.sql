INSERT
    INTO
        content.film_files (
            uuid
            ,resolution
            ,film_id
            ,destination_path
            ,updated_at
        )
    VALUES {}
        ON CONFLICT (uuid) DO NOTHING
;