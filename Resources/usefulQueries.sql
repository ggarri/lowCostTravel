-- FALSE to not flight airport
SELECT *
FROM coreBundle_flight
WHERE edreams_geoId_out IN (select edreams_geoId from coreBundle_airport where country_id = 43 and is_main=true)
ORDER by price asc, duration_in desc

-- RESET
UPDATE coreBundle_airport set is_main = true where country_id = 43

-- Flights GO
SELECT *
FROM coreBundle_flight
WHERE edreams_geoId_out IN (select edreams_geoId from coreBundle_airport where country_id = 52 and is_main=true)
and price <> -1
ORDER BY price asc, duration_in desc

-- Flights BACK
SELECT *
FROM coreBundle_flight
WHERE edreams_geoId_in IN (select edreams_geoId from coreBundle_airport where country_id = 52 and is_main=true)
and price <> -1
ORDER BY price asc, duration_in desc

-- Flights Go-BACK
SELECT *
FROM coreBundle_flight
WHERE edreams_geoId_in IN (select edreams_geoId from coreBundle_airport where country_id = 52 and is_main=true)
and price <> -1 and trip_type <> 'ONE_WAY'
ORDER BY price asc, duration_in desc

-- Flights Go-BACK by country code
SELECT a2.code, a.code, f.*
FROM coreBundle_country c
INNER JOIN coreBundle_airport a ON (a.country_id = c.id)
INNER JOIN coreBundle_flight f ON (f.edreams_geoId_in = a.edreams_geoId OR f.edreams_geoId_out = a.edreams_geoId)
INNER JOIN coreBundle_airport a2 ON (a2.edreams_geoId = f.edreams_geoId_out OR a2.edreams_geoId = f.edreams_geoId_in)
WHERE c.code = 'CU' AND f.price <> -1
ORDER BY f.trip_type <> 'ONE_WAY' DESC, f.price asc, f.duration_in desc


