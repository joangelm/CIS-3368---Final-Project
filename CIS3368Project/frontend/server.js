// Adding necessary modules
const express = require("express");
const app = express();
const axios = require("axios");
const bodyParser = require("body-parser");
const { cache } = require("ejs");

// Set the view engine to EJS
app.set("view engine", "ejs");

app.use(
    bodyParser.urlencoded({
        extended: true,
    })
);

app.get("/cargo", (req, res) => {
    const error = req.query.error;
    axios.get(`http://127.0.0.1:5000/api/cargo/all`).then((response) => {
        var cargo = response.data;
        var tagline = "The list of cargo";
        // use res.render to load up an ejs view file
        if (error) {
            res.render("pages/cargo.ejs", {
                cargo: cargo,
                tagline: tagline,
                error: error,
            });
        } else {
            res.render("pages/cargo.ejs", {
                cargo: cargo,
                tagline: tagline,
            });
        }
    });
});

app.get("/spaceship", (req, res) => {
    const error = req.query.error;
    axios.get(`http://127.0.0.1:5000/api/spaceship/all`).then((response) => {
        var spaceship = response.data;
        var tagline = "The list of spaceships";
        // use res.render to load up an ejs view file
        if (error) {
            res.render("pages/spaceship.ejs", {
                spaceship: spaceship,
                tagline: tagline,
                error: error,
            });
        } else {
            res.render("pages/spaceship.ejs", {
                spaceship: spaceship,
                tagline: tagline,
            });
        }
    });
});

app.get("/captain", (req, res) => {
    const error = req.query.error;
    axios.get(`http://127.0.0.1:5000/api/captain/all`).then((response) => {
        var captain = response.data;
        var tagline = "The list of captains";
        // use res.render to load up an ejs view file
        if (error) {
            res.render("pages/captain.ejs", {
                captain: captain,
                tagline: tagline,
                error: error,
            });
        } else {
            res.render("pages/captain.ejs", {
                captain: captain,
                tagline: tagline,
            });
        }
    });
});

// Index Page
app.get("/", (req, res) => {
    res.render("pages/index.ejs");
});

app.post("/process_login", async function (req, res) {
    var user = req.body.username;
    var password = req.body.password;

    const response = await axios.get("http://127.0.0.1:5000/authenticatedroute", { auth: { username: user, password: password } });
    console.log(response.status);
    if (response.status == 200) {
        res.redirect("/cargo");
    } else {
        res.render("/", {
            user: "UNAUTHORIZED",
            auth: false,
        });
    }
});

// Cargo Page
app.post("/api/cargo", async function (req, res) {
    var weight = req.body.weight;
    var cargotype = req.body.cargotype;
    var departure = req.body.departure;
    var arrival = req.body.arrival;
    var shipid = req.body.shipid;
    try {
        await axios.post(`http://127.0.0.1:5000/api/cargo`, { weight, cargotype, departure, arrival, shipid });
        res.redirect("back");
    } catch (error) {
        res.redirect("/cargo?error=" + "maxweight");
    }
});

app.post("/api/cargo/update", async function (req, res) {
    var id = req.body.cargoid;
    var weight = req.body.weight;
    var cargotype = req.body.cargotype;
    var departure = req.body.departure;
    var arrival = req.body.arrival;
    var shipid = req.body.shipid;
    await axios.put(`http://127.0.0.1:5000/api/cargo`, { id, weight, cargotype, departure, arrival, shipid });
    res.redirect("back");
});

app.post("/api/cargo/delete", async function (req, res) {
    var id = req.body.cargoid;
    await axios.delete(`http://127.0.0.1:5000/api/cargo`, { params: { id } });
    res.redirect("back");
});

// Spaceship Page
app.post("/api/spaceship", async function (req, res) {
    var maxweight = req.body.maxweight;
    var captainid = req.body.captainid;
    try {
        await axios.post(`http://127.0.0.1:5000/api/spaceship`, { maxweight, captainid });
        res.redirect("back");
    } catch (error) {
        res.redirect("/spaceship?error=");
    }
});

app.post("/api/spaceship/update", async function (req, res) {
    var id = req.body.spaceshipid;
    var maxweight = req.body.maxweight;
    var captainid = req.body.captainid;
    await axios.put(`http://127.0.0.1:5000/api/spaceship`, { id, maxweight, captainid });
    res.redirect("back");
});

app.post("/api/spaceship/delete", async function (req, res) {
    var id = req.body.spaceshipid;
    await axios.delete(`http://127.0.0.1:5000/api/spaceship`, { params: { id } });
    res.redirect("back");
});

// Captain Page
app.post("/api/captain", async function (req, res) {
    var firstname = req.body.firstname;
    var lastname = req.body.lastname;
    var rankstatus = req.body.rankstatus;
    var homeplanet = req.body.homeplanet;
    try {
        await axios.post(`http://127.0.0.1:5000/api/captain`, { firstname, lastname, rankstatus, homeplanet });
        res.redirect("back");
    } catch (error) {
        res.redirect("/captain?error=");
    }
});

app.post("/api/captain/update", async function (req, res) {
    var id = req.body.captainid;
    var firstname = req.body.firstname;
    var lastname = req.body.lastname;
    var rankstatus = req.body.rankstatus;
    var homeplanet = req.body.homeplanet;
    await axios.put(`http://127.0.0.1:5000/api/captain`, { id, firstname, lastname, rankstatus, homeplanet });
    res.redirect("back");
});

app.post("/api/captain/delete", async function (req, res) {
    var id = req.body.captainid;
    await axios.delete(`http://127.0.0.1:5000/api/captain`, { params: { id } });
    res.redirect("back");
});

// Port selected to listen
app.listen(8080, () => console.log("Listening on port 8080"));
