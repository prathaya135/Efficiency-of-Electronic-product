import Router  from "next/router";
import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:4000/api/users/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      const data = await response.json();
      console.log(data);
      Router.push("/Home"); // Redirect to home page on successful login
      // Handle login success (store token, redirect, etc.)
      localStorage.setItem("token", data.token); // Store token in local storage
    } catch (error) {
      console.error("Login failed", error);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-green-100 px-4">
      <div className="flex flex-col md:flex-row bg-white p-8 rounded-2xl shadow-lg max-w-4xl w-full">
        {/* Left Side - Form */}
        <div className="md:w-1/2 w-full mt-8">
          <h2 className="text-2xl font-bold text-center text-green-700 mb-6">Login</h2>
          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label htmlFor="email" className="block text-gray-700">
                Email
              </label>
              <input
                id="email"
                type="email"
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400 placeholder-gray-500 text-gray-700 text-sm"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="password" className="block text-gray-700">
                Password
              </label>
              <input
                id="password"
                type="password"
                className="w-full p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-400 placeholder-gray-500 text-gray-700 text-sm"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              className="w-full mt-4 bg-green-600 text-white p-2 rounded-lg hover:bg-green-700 transition"
            >
              Login
            </button>
            <p className="text-center text-sm text-gray-600 mt-4">
              Don't have an account?{" "}
              <a href="/SignUp" className="text-green-600 hover:underline">
                Sign Up
              </a>
            </p>
          </form>
        </div>

        {/* Right Side - Image */}
        <div className="md:w-1/2 w-full flex items-center justify-center mt-8 md:mt-0">
          <img
            src="/images/logimage.png"
            alt="Person interacting with login interface"
            className="w-full max-w-sm h-auto"
          />
        </div>
      </div>
    </div>
  );
}
