"use client";

import Navbar from "../../components/Navbar/Navbar";
import Image from "next/image";
import { motion } from "framer-motion";

export default function About() {
  const teamMembers = [
    { name: "Swanand Joshi", image: "/images/swanand.jpg" },
    { name: "Aditya Gade", image: "/images/aditya.jpg" },
    { name: "Sudhanshu", image: "/images/sudhanshu.jpg" },
    { name: "Prathamesh Patil", image: "/images/prathamesh.jpg" },
  ];

  return (
    <>
      <Navbar />
      <div className="bg-gradient-to-b from-blue-100 to-white min-h-screen py-12 px-6 text-center">
        {/* Our Vision & Mission */}
        <div className="max-w-4xl mx-auto text-gray-700 space-y-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
            className="bg-white shadow-lg rounded-xl p-6"
          >
            <h2 className="text-3xl font-semibold text-blue-700 mb-3">Our Vision</h2>
            <p className="text-lg">
              We aim to revolutionize sustainability using cutting-edge AI solutions,
              creating a greener, more efficient world for future generations.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            viewport={{ once: true }}
            className="bg-white shadow-lg rounded-xl p-6"
          >
            <h2 className="text-3xl font-semibold text-blue-700 mb-3">Our Mission</h2>
            <p className="text-lg">
              Our mission is to optimize resource utilization through AI-driven innovation,
              reducing environmental impact and promoting sustainable development.
            </p>
          </motion.div>
        </div>

        {/* Team Section */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          viewport={{ once: true }}
          className="mt-16"
        >
          <h2 className="text-4xl font-semibold text-indigo-700 mb-8">Meet Our Team</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8 max-w-5xl mx-auto">
            {teamMembers.map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.4, delay: index * 0.2 }}
                viewport={{ once: true }}
                className="bg-white shadow-lg rounded-xl p-4 transform hover:scale-105 transition duration-300"
              >
                <Image
                  src={member.image}
                  alt={member.name}
                  width={150}
                  height={150}
                  className="w-32 h-32 object-cover mx-auto rounded-full border-4 border-indigo-500"
                />
                <h3 className="mt-4 text-xl font-bold text-gray-800">{member.name}</h3>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </>
  );
}
