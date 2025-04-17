import Image from 'next/image';
import { motion } from 'framer-motion';
import Navbar from '@/components/Navbar/Navbar';

export default function Home() {
  return (
    <>
    <Navbar></Navbar>
    <div className="min-h-screen bg-gradient-to-b from-green-200 to-white flex flex-col items-center justify-center p-6">
      {/* Hero Section */}
      <motion.div 
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center max-w-3xl"
      >
        <h1 className="text-5xl font-extrabold text-green-900 mb-4">
          Sustainable AI for a Greener Future
        </h1>
        <p className="text-lg text-gray-700">
          Our AI model leverages <span className='font-bold'>reinforcement learning</span> to <span className='font-bold'>enhance product sustainability</span>, 
          optimizing resources and reducing environmental impact.  
        </p>
      </motion.div>

    <div className='flex justify-between items-center gap-4'>
      {/* <motion.div 
        initial={{ opacity: 0, scale: 0.8 }} 
        animate={{ opacity: 1, scale: 1 }} 
        transition={{ duration: 0.8 }}
      >
        <Image src="/images/image2.png" width={210} height={210} alt="AI Sustainability" className="rounded-lg shadow-md mt-10" />
      </motion.div> */}

      {/* How It Works Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 1 }}
        className="mt-10 max-w-4xl bg-white p-6 shadow-xl rounded-2xl"
      >
        <h2 className="text-3xl font-semibold text-green-900 text-center">How It Works</h2>
        <p className="text-lg text-gray-700 mt-4 leading-relaxed text-left">
          1. <span className='font-bold'>Data Collection:</span> The model analyzes product lifecycle and sustainability metrics. <br/>
          2. <span className='font-bold'>Reinforcement Learning:</span> AI optimizes product designs and materials for maximum efficiency. <br/>
          3. <span className='font-bold'>impact Measurement:</span> Evaluates environmental savings and suggests further improvements. <br/>
          4. <span className='font-bold'>Deployment:</span> Sustainable recommendations are integrated into production and supply chains.
        </p>
      </motion.div>
      {/* <motion.div 
        initial={{ opacity: 0, scale: 0.8 }} 
        animate={{ opacity: 1, scale: 1 }} 
        transition={{ duration: 0.8 }}
      >
        <Image src="/images/image2.png" width={210} height={210} alt="AI Sustainability" className="rounded-lg shadow-md mt-10" />
      </motion.div> */}
      </div>

      {/* Images Section */}
      <div className="min-h-screen flex flex-col items-center p-6">
        {/* Introduction Section */}

        {/* Image Section with Animation */}
        <div className="mt-10 flex items-center justify-center gap-6">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center max-w-3xl"
          >
            <h1 className="text-4xl font-bold text-gray-900 mb-4">Enhancing Product Sustainability with AI</h1>
            <p className="text-lg text-gray-600">
              Our AI-powered system optimizes product sustainability using reinforcement learning. By analyzing data, 
              it recommends eco-friendly materials, reduces waste, and maximizes efficiency, ensuring long-term sustainability.
            </p>
          </motion.div>
          {/* <motion.div 
            initial={{ opacity: 0, scale: 0.8 }} 
            animate={{ opacity: 1, scale: 1 }} 
            transition={{ duration: 0.8 }}
          >
            <Image src="/images/image2.png" width={300} height={300} alt="AI Sustainability" className="rounded-lg shadow-md" />
          </motion.div> */}

          {/* <motion.div 
            initial={{ opacity: 0, scale: 0.8 }} 
            animate={{ opacity: 1, scale: 1 }} 
            transition={{ duration: 0.9 }}
          >
            <Image src="/images/image3.png" width={400} height={300} alt="Reinforcement Learning" className="rounded-lg shadow-md" />
          </motion.div> */}

        </div>

        {/* Grid Image Section with Animation */}
        <div className="mt-10 grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { src: "/images/ai-sustainability.png", alt: "AI Sustainability" },
            { src: "/images/image1.png", alt: "Reinforcement Learning" },
            { src: "/images/image2.png", alt: "Reinforcement Learning" }
          ].map((image, index) => (
            <motion.div 
              key={index}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 1 + index * 0.2 }}
            >
              <Image src={image.src} width={300} height={200} alt={image.alt} className="rounded-lg shadow-md" />
            </motion.div>
          ))}
        </div>
      </div>
    </div>
    </>
  );
}
