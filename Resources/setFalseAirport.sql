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
WHERE edreams_geoId_out IN (select edreams_geoId from coreBundle_airport where country_id = 43 and is_main=true)
ORDER BY price asc, duration_in desc

-- Flights BACK
SELECT *
FROM coreBundle_flight
WHERE edreams_geoId_in IN (select edreams_geoId from coreBundle_airport where country_id = 43 and is_main=true)
ORDER BY price asc, duration_in desc

