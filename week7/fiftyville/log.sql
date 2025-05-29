-- Keep a log of any SQL queries you execute as you solve the mystery.

-- check description of crime scene report on Humphrey Street.
SELECT id, description FROM crime_scene_reports WHERE day = 28 AND month = 7 AND year = 2024 AND street = 'Humphrey Street';
-- found:
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. 
-- Interviews were conducted today with three witnesses who were present
-- at the time – each of their interview transcripts mentions the bakery.
-- todo: check witness interviews

-- check witness interviews
SELECT id, name, transcript FROM interviews WHERE day = 28 AND month = 7 AND year = 2024 AND transcript LIKE '%bakery%;
-- found:
-- Ruth	Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene	I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- Raymond	As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- Ruth -> check security footage
SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2024 AND hour = 10 AND minute >=15 AND minute <= 25 AND activity = "exit";
-- found:
-- 5P2BI95
-- 94KL13X
-- 6P58WS2
-- 4328GD8
-- G412CB7
-- L93JTIZ
-- 322W7JE
-- 0NTHK55

-- Eugene -> check ATM logs
SELECT DISTINCT person_id, account_number FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND year = 2024 AND atm_location LIKE "%Leggett%" AND transaction_type = "withdraw");
-- found:
-- person_id	account_number
-- 686048	    49610011
-- 514354	    26013199
-- 458378	    16153065
-- 395717	    28296815
-- 396669	    25506511
-- 467400	    28500762
-- 449774	    76054385
-- 438727	    81061156

-- Raymond -> check phone call logs
SELECT caller, receiver FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60;
-- found:
-- caller           	receiver
-- (130) 555-0289	(996) 555-8899
-- (499) 555-9472	(892) 555-8872
-- (367) 555-5533	(375) 555-8161
-- (609) 555-5876	(389) 555-5198
-- (499) 555-9472	(717) 555-1342
-- (286) 555-6063	(676) 555-6554
-- (770) 555-1861	(725) 555-3243
-- (031) 555-6622	(910) 555-3251
-- (826) 555-1652	(066) 555-9701
-- (338) 555-6650	(704) 555-2131

-- find thief candidates from caller phone_calls, license plate from camera footage and withdrawal from ATM logs
SELECT name, passport_number FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2024 AND hour = 10 AND minute >=15 AND minute <= 25 AND activity = "exit");
-- thief_candidates:
-- Diana	3592750733
-- Bruce	5773159633

-- check if any of the thief candidates have a flight booked for tomorrow morning
SELECT name FROM people WHERE passport_number IN (SELECT passport_number FROM flights, passengers WHERE flights.id = passengers.flight_id AND passengers.passport_number IN (SELECT passport_number FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2024 AND hour = 10 AND minute >=15 AND minute <= 25 AND activity = "exit") AND id IN (SELECT DISTINCT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND year = 2024 AND atm_location LIKE "%Leggett%" AND transaction_type = "withdraw"))) ORDER BY flights.year, flights.month, flights.day, flights.hour, flights.minute LIMIT 1);
-- found: Bruce as the only candidate with a flight booked for tomorrow morning.

-- check Bruce going to
SELECT city FROM airports WHERE id IN (SELECT destination_airport_id FROM flights, passengers WHERE flights.id = passengers.flight_id AND passengers.passport_number IN (SELECT passport_number FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2024 AND hour = 10 AND minute >=15 AND minute <= 25 AND activity = "exit") AND id IN (SELECT DISTINCT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND year = 2024 AND atm_location LIKE "%Leggett%" AND transaction_type = "withdraw"))) ORDER BY flights.year, flights.month, flights.day, flights.hour, flights.minute LIMIT 1);
-- found: New York City

-- check who Bruce accomplice is
SELECT name FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60 AND caller IN (SELECT phone_number FROM people WHERE passport_number IN (SELECT passport_number FROM flights, passengers WHERE flights.id = passengers.flight_id AND passengers.passport_number IN (SELECT passport_number FROM people WHERE phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND year = 2024 AND duration <= 60) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE day = 28 AND month = 7 AND year = 2024 AND hour = 10 AND minute >=15 AND minute <= 25 AND activity = "exit") AND id IN (SELECT DISTINCT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND year = 2024 AND atm_location LIKE "%Leggett%" AND transaction_type = "withdraw"))) ORDER BY flights.year, flights.month, flights.day, flights.hour, flights.minute LIMIT 1)));
-- found: Robin as the accomplice of Bruce.