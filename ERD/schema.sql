CREATE TABLE IF NOT EXISTS "Πελάτης" (
	"Email" string,
	"Κάρτα" string,
	"Ονοματεπώνυμο" string,
	"Κωδικός Λογαριασμού" string,
	"Διεύθυνση?" string,
	PRIMARY KEY ("Email")
);

CREATE TABLE IF NOT EXISTS "Κατάστημα" (
	"Κωδικός Καταστήματος" integer,
	"Ωράριο" string,
	"Διεύθυνση" string,
	"Κριτική" decimal,
	PRIMARY KEY ("Κωδικός Καταστήματος")
);

CREATE TABLE IF NOT EXISTS "Κατηγορία" (
	"Όνομα" string,
	PRIMARY KEY ("Όνομα")
);

CREATE TABLE IF NOT EXISTS "Ντελιβεράς" (
	"ΑΦΜ" integer,
	"Διαθεσιμοτητα" boolean,
	PRIMARY KEY ("ΑΦΜ")
);

CREATE TABLE IF NOT EXISTS "Εξυπηρέτηση Πελατών" (
	"ΑΦΜ" integer,
	"Διαθεσιμότητα" boolean,
	PRIMARY KEY ("ΑΦΜ")
);

CREATE TABLE IF NOT EXISTS "Ανήκει" (
	"Όνομα Κατηγορίας" string,
	"Όνομα Πιάτου" string,
	FOREIGN KEY ("Όνομα Κατηγορίας") REFERENCES "Κατηγορία" ("Όνομα")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("Όνομα Πιάτου") REFERENCES "Πιάτο" ("Όνομα")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Περιέχει" (
	"Κωδικός Παραγγελίας" integer,
	"Κωδικός Καταστήματος" integer,
	"Όνομα Πιάτου" string,
	"Ποσότητα" integer,
	FOREIGN KEY ("Κωδικός Παραγγελίας") REFERENCES "Παραγγελία" ("Κωδικός Παραγγελίας")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("Κωδικός Καταστήματος") REFERENCES "Πιάτο" ("Κωδικός Καταστήματος(Φτιάχνει)")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("Όνομα Πιάτου") REFERENCES "Πιάτο" ("Όνομα")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Αξιολογεί" (
	"" 
);

CREATE TABLE IF NOT EXISTS "Ορίζει Αγαπημένο" (
	"Κωδικός Καταστήματος" integer,
	"Email" string,
	FOREIGN KEY ("Κωδικός Καταστήματος") REFERENCES "Κατάστημα" ("Κωδικός Καταστήματος")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("Email") REFERENCES "Πελάτης" ("Email")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Πιάτο" (
	"Όνομα" string,
	"Κωδικός Καταστήματος(Φτιάχνει)" integer,
	"Διαθεσιμότητα" boolean,
	"Τιμή" decimal,
	PRIMARY KEY ("Όνομα", "Κωδικός Καταστήματος(Φτιάχνει)"),
	FOREIGN KEY ("Κωδικός Καταστήματος(Φτιάχνει)") REFERENCES "Κατάστημα" ("Κωδικός Καταστήματος")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Παραγγελία" (
	"Κωδικός Παραγγελίας" integer,
	"Αλλεργίες" text,
	"Email Πελάτη" string,
	"ΑΦΜ Ντελιβερά" integer,
	"Ώρα Παραγγελίας" timestamp,
	"Ημερομηνία Παραγγελίας" date,
	"Ώρα Αξιολόγησης" timestamp,
	"Κείμενο Αξιολόγησης" text,
	"Σκορ Αξιολόγησης" decimal,
	"Ώρα Παραλαβής " timestamp,
	"Χρόνος Παράδοσης " timestamp,
	"Πραγματικός Χρόνος Παράδοσης" timestamp,
	PRIMARY KEY ("Κωδικός Παραγγελίας"),
	FOREIGN KEY ("Email Πελάτη") REFERENCES "Πελάτης" ("Email")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("ΑΦΜ Ντελιβερά") REFERENCES "Ντελιβεράς" ("ΑΦΜ")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS "Αίτηση Αλλαγής" (
	"Κωδικός Αίτησης" integer,
	"Κωδικός Παραγγελίας" integer,
	"Email Πελάτη" string,
	"ΑΦΜ Υπαλλήλου" integer,
	"Ώρα" timestamp,
	"Τρόπος" string,
	PRIMARY KEY ("Κωδικός Αίτησης"),
	FOREIGN KEY ("Κωδικός Παραγγελίας") REFERENCES "Παραγγελία" ("Κωδικός Παραγγελίας")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("Email Πελάτη") REFERENCES "Πελάτης" ("Email")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT,
	FOREIGN KEY ("ΑΦΜ Υπαλλήλου") REFERENCES "Εξυπηρέτηση Πελατών" ("ΑΦΜ")
            ON UPDATE RESTRICT
            ON DELETE RESTRICT
);

