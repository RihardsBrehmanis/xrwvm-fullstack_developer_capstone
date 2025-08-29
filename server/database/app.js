const express = require('express');
const mongoose = require('mongoose');
const fs = require('fs');
const cors = require('cors')
const app = express()
const port = 3030;

// Use CORS and body-parser middleware
app.use(cors())
app.use(express.json()); // Use express.json() for parsing JSON bodies
app.use(express.urlencoded({ extended: false }));

// Read data from JSON files
const reviews_data = JSON.parse(fs.readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(fs.readFileSync("dealerships.json", 'utf8'));

// Connect to MongoDB
mongoose.connect("mongodb://mongo_db:27017/",{'dbName':'dealershipsDB'});

// Import Mongoose models
const Reviews = require('./review');
const Dealerships = require('./dealership');

// Asynchronously load initial data into the database if collections are empty.
// This is done on server startup.
async function loadData() {
    try {
        const reviewCount = await Reviews.countDocuments();
        if (reviewCount === 0) {
            await Reviews.deleteMany({});
            await Reviews.insertMany(reviews_data['reviews']);
            console.log("Reviews data loaded successfully.");
        } else {
            console.log("Reviews data already exists, skipping load.");
        }

        // --- NEW LOGIC FOR DEALERSHIP DATA LOADING ---
        // Always delete existing dealerships to ensure the latest data is loaded
        await Dealerships.deleteMany({});
        await Dealerships.insertMany(dealerships_data['dealerships']);
        console.log("Dealerships data reloaded successfully.");
        // --- END OF NEW LOGIC ---
    } catch (error) {
        console.error('Error loading initial data:', error);
    }
}
loadData();


// Express route to home
app.get('/', async (req, res) => {
    res.send("Welcome to the Mongoose API")
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
    try {
        const documents = await Reviews.find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
    try {
        // Fetch reviews by the 'dealership' field, which contains the dealer ID
        const documents = await Reviews.find({ dealership: req.params.id });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching documents' });
    }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
    try {
        const documents = await Dealerships.find();
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: 'Error fetching dealerships' });
    }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
    try {
        const documents = await Dealerships.find({
            $or: [
                { st: req.params.state },
                { state: req.params.state }
            ]
        });
        res.json(documents);
    } catch (error) {
        res.status(500).json({ error: `Error fetching dealerships for state ${req.params.state}` });
    }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
    try {
        const document = await Dealerships.findOne({ id: req.params.id });
        if (!document) {
            return res.status(404).json({ error: 'Dealer not found' });
        }
        res.json(document);
    } catch (error) {
        res.status(500).json({ error: `Error fetching dealer with ID ${req.params.id}` });
    }
});

// Express route to insert review
app.post('/insert_review', async (req, res) => {
    try {
        // Find the highest existing ID to create a new one
        const latestReview = await Reviews.findOne().sort({ id: -1 });
        let new_id = 1;
        if (latestReview) {
            new_id = latestReview.id + 1;
        }

        const data = req.body;
        const review = new Reviews({
            "id": new_id,
            "name": data['name'],
            "dealership": data['dealership'],
            "review": data['review'],
            "purchase": data['purchase'],
            "purchase_date": data['purchase_date'],
            "car_make": data['car_make'],
            "car_model": data['car_model'],
            "car_year": data['car_year'],
        });

        const savedReview = await review.save();
        res.status(201).json(savedReview);
    } catch (error) {
        console.log(error);
        res.status(500).json({ error: 'Error inserting review' });
    }
});

// Start the Express server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
