import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Navbar from "../../components/Navbar/Navbar";

const TypingText = ({ text = "", delay = 0, onComplete }) => {
  const [displayedText, setDisplayedText] = useState("");

  useEffect(() => {
    setDisplayedText("");
    let index = 0;
    const interval = setInterval(() => {
      if (index < text.length) {
        setDisplayedText((prev) => prev + text[index]);
        index++;
      } else {
        clearInterval(interval);
        if (onComplete) onComplete(); // Notify when typing animation is done
      }
    }, 50);

    return () => clearInterval(interval);
  }, [text]);

  return (
    <motion.p
      className="text-gray-700"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1, delay }}
    >
      {displayedText}
    </motion.p>
  );
};

export default function Services() {
  const [deviceType, setDeviceType] = useState("");
  const [inputFields, setInputFields] = useState([]);
  const [inputs, setInputs] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showFinalResult, setShowFinalResult] = useState(false);

  const handleDeviceSelection = async (event) => {
    const selectedDevice = event.target.value;
    setDeviceType(selectedDevice);
    setInputFields([]);
    setInputs({});
    setResult(null);
    setShowFinalResult(false);

    if (!selectedDevice) return;

    try {
      const response = await fetch("http://127.0.0.1:5000/select-device", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ device_type: selectedDevice }),
      });

      const data = await response.json();
      if (response.ok) {
        setInputFields(data.input_fields);
        setInputs(Object.fromEntries(data.input_fields.map((field) => [field, ""])));
      } else {
        console.error(data.error);
      }
    } catch (error) {
      console.error("Error fetching device inputs:", error);
    }
  };

  const handleInputChange = (field, value) => {
    setInputs((prev) => ({ ...prev, [field]: value }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setShowFinalResult(false);
    const formattedInputs = Object.values(inputs);
    
    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ device_type: deviceType, inputs: formattedInputs }),
      });

      const data = await response.json();
      setTimeout(() => {
        setLoading(false);
        if (response.ok) {
          setResult(data);
        } else {
          console.error(data.error);
        }
      }, 2000);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />
      <div
  className="relative flex flex-col min-h-screen "
  style={{
    backgroundImage: "url('/backgroundServices.png')",
    backgroundSize: "cover",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "center",
  }}
>
  <div className="absolute inset-0 bg-white/70 backdrop-blur-md z-0"></div>
   <div className="relative z-10">
      <div className="flex flex-col mb-10">
        <motion.div
          className="flex flex-col items-center"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <label className="text-lg font-semibold text-gray-500">Select Device:</label>
          <select
            className="mt-2 p-2 border border-gray-300 rounded-lg text-gray-800 bg-white shadow-md"
            onChange={handleDeviceSelection}
            value={deviceType}
          >
            <option value="">-- Select --</option>
            {[
              "Laptop", "Tablet", "Smartphone", "Desktop Computer",
              "Smartwatch", "E-Reader", "Wearable Fitness Tracker",
              "Television", "Digital Camera", "Printer", "Scanner",
              "Smart Home Assistant"
            ].map((device, index) => (
              <option key={index} value={device}>{device}</option>
            ))}
          </select>
        </motion.div>

        <div className="mr-5 ml-5">
          <AnimatePresence>
            {inputFields.length > 0 && (
              <motion.div
                className="mt-5 bg-white p-6 shadow-lg rounded-lg border border-gray-300 w-full"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.5 }}
              >
                <h2 className="text-xl font-semibold text-gray-800">Enter Details:</h2>

                <div className="grid grid-cols-1 sm:grid-cols-3 md:grid-cols-3 gap-4 mt-4">
                  {inputFields.map((field, index) => (
                    <motion.div
                      key={index}
                      className="flex flex-col"
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <label className="font-medium text-gray-700" >{field}:</label>
                      <input
                        type="text"
                        className="mt-1 p-2 border border-gray-300 rounded-lg text-gray-800 shadow-sm"
                        value={inputs[field] || ""}
                        onChange={(e) => handleInputChange(field, e.target.value)}
                      />
                    </motion.div>
                  ))}
                </div>

                <motion.button
                  className="mt-5 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-lg hover:bg-blue-700 transition-all"
                  onClick={handleSubmit}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  Predict
                </motion.button>
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {loading && (
              <motion.div
                className="mt-5 text-lg font-semibold text-gray-700"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                ⏳ Generating prediction...
              </motion.div>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {result && !loading && !showFinalResult && (
              <motion.div
                className="mt-8 p-6 border border-gray-400 rounded-lg shadow-lg bg-white w-96"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                <h2 className="text-xl font-bold text-gray-800">Prediction Results</h2>

                <TypingText text={`Device Type: ${result.device_type || "N/A"}`} delay={0} onComplete={() => setTimeout(() => setShowFinalResult(true), 1000)} />
                <TypingText text={`Sustainability Score: ${result.sustainability ?? "N/A"}`} delay={1} />
                <TypingText text={`Estimated Lifespan: ${result.lifespan ? `${result.lifespan} years` : "N/A"}`} delay={2} />
              </motion.div>
            )}
          </AnimatePresence>

          {/* {showFinalResult && result && (
            <motion.div
              className="mt-8 p-6 border border-gray-400 rounded-lg shadow-lg bg-white w-96"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h2 className="text-xl font-bold text-gray-800">Final Prediction Results</h2>
              <p className="text-gray-700">Device Type: {result.device_type || "N/A"}</p>
              <p className="text-gray-700">Sustainability Score: {result.sustainability ?? "N/A"}</p>
              <p className="text-gray-700">Estimated Lifespan: {result.lifespan ? `${result.lifespan} years` : "N/A"}</p>
              <ul className="list-disc ml-5 text-gray-700">
                {Array.isArray(result.suggestions) && result.suggestions.length > 0 ? (
                  result.suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))
                ) : (
                  <p>No suggestions available</p>
                )}
              </ul>
            </motion.div>
          )} */}
          {showFinalResult && result && (
            <motion.div
              className="mt-8 p-6 border border-gray-400 rounded-lg shadow-lg bg-white w-full"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h2 className="text-xl font-bold text-gray-800">Final Prediction Results</h2>

              {/* Device Details Box */}
              <div className=" flex items-center justify-around">
                <div className="mt-4 p-4 border border-gray-300 rounded-lg bg-gray-100">
                  <p className="text-gray-700"><span className="font-semibold">Device Type:</span> {result.device_type || "N/A"}</p>
                  <p className="text-gray-700"><span className="font-semibold">Sustainability Score:</span> {result.sustainability ?? "N/A"}</p>
                  <p className="text-gray-700"><span className="font-semibold">Estimated Lifespan:</span> {result.lifespan ? `${result.lifespan} years` : "N/A"}</p>
                </div>

                {/* Suggestions Box */}
                <div className="mt-4 p-4 border border-gray-300 rounded-lg bg-gray-100">
                  <h3 className="font-semibold text-gray-800">Suggestions:</h3>
                  {Array.isArray(result.suggestions) && result.suggestions.length > 0 ? (
                    <ul className="list-disc ml-5 text-gray-700">
                      {result.suggestions.map((suggestion, index) => (
                        <li key={index}>{suggestion}</li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-gray-700">No suggestions available</p>
                  )}
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </div>
      </div>
      </div>
    </>
  );
}
