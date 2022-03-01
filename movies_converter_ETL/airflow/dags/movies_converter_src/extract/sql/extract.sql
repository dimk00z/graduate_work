SELECT fw.film_id as fw_id, file_name, fw.destination_path, source_path, source_resolution, ARRAY_AGG(DISTINCT ff.resolution) AS resolutions
FROM content.film_work fw, content.film_files ff
WHERE fw.film_id = ff.film_id
GROUP BY fw_id;