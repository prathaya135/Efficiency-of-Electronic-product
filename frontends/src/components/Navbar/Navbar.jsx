"use client";
import { useState } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Menu, X, Home, Briefcase, MessageSquare, Info } from "lucide-react";

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  const navItems = [
    { name: "Home", href: "/Home", icon: <Home size={20} /> },
    { name: "Services", href: "/Services", icon: <Briefcase size={20} /> },
    { name: "Feedback", href: "/Feedback", icon: <MessageSquare size={20} /> },
    { name: "About", href: "/About", icon: <Info size={20} /> },
  ];

  return (
    <nav className="bg-gradient-to-r from-blue-500 to-indigo-600 p-4 shadow-md sticky top-0 z-50 backdrop-blur-lg">
      <div className="container mx-auto flex justify-between items-center">
        {/* Logo */}
        <h1 className="text-white text-3xl font-extrabold tracking-wide">
          EcoOptimizer 🌍
        </h1>

        {/* Desktop Menu */}
        <ul className="hidden md:flex space-x-6">
          {navItems.map((item, index) => (
            <motion.li
              key={item.name}
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="relative flex items-center space-x-2"
            >
              {item.icon}
              <Link
                href={item.href}
                className="text-white text-lg font-medium hover:text-gray-200 transition-all duration-300"
              >
                {item.name}
              </Link>
              {/* Underline Animation */}
              <motion.div
                className="absolute bottom-0 left-0 w-full h-[2px] bg-white scale-x-0"
                whileHover={{ scaleX: 1 }}
                transition={{ duration: 0.3 }}
              />
            </motion.li>
          ))}
        </ul>

        {/* Mobile Menu Button */}
        <button
          className="md:hidden text-white focus:outline-none"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X size={28} /> : <Menu size={28} />}
        </button>
      </div>

      {/* Mobile Menu Dropdown */}
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
          className="md:hidden flex flex-col items-center bg-blue-500/90 backdrop-blur-lg p-4 rounded-lg mt-2 shadow-lg"
        >
          {navItems.map((item) => (
            <Link
              key={item.name}
              href={item.href}
              className="flex items-center space-x-2 text-white text-lg py-2 hover:text-gray-200 transition-all duration-300"
              onClick={() => setIsOpen(false)}
            >
              {item.icon} <span>{item.name}</span>
            </Link>
          ))}
        </motion.div>
      )}
    </nav>
  );
};

export default Navbar;
