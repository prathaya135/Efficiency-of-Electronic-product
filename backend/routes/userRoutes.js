const express = require('express');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('../models/User');
const sendOTPEmail = require('../utils/email');

const router = express.Router();

// Signup - Step 1: Send OTP
router.post('/signup', async (req, res) => {
    const { name, email, password, confirmPassword } = req.body;

    if (password !== confirmPassword) {
        return res.status(400).json({ message: 'Passwords do not match' });
    }

    const existingUser = await User.findOne({ email });
    if (existingUser) {
        return res.status(400).json({ message: 'Email already exists' });
    }

    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const otpExpires = new Date(Date.now() + 5 * 60 * 1000); // Expires in 5 mins

    const newUser = new User({ name, email, password, otp, otpExpires, isVerified: false });

    await sendOTPEmail(email, otp); // Send OTP to email
    await newUser.save();

    res.status(200).json({ message: 'OTP sent to email. Please verify.' });
});

// Verify OTP - Step 2
router.post('/verify-otp', async (req, res) => {
    const { email, otp } = req.body;

    const user = await User.findOne({ email, otp, otpExpires: { $gt: new Date() } });
    if (!user) {
        return res.status(400).json({ message: 'Invalid or expired OTP' });
    }

    user.isVerified = true;
    user.otp = undefined;
    user.otpExpires = undefined;
    
    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(user.password, salt); // Hash password

    await user.save();
    res.status(200).json({ message: 'Account verified. You can now log in.' });
});

// Login
router.post('/login', async (req, res) => {
    const { email, password } = req.body;

    const user = await User.findOne({ email, isVerified: true });
    if (!user) {
        return res.status(400).json({ message: 'Invalid email or account not verified' });
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
        return res.status(400).json({ message: 'Invalid password' });
    }

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    res.status(200).json({ token, message: 'Login successful' });
});

module.exports = router;
