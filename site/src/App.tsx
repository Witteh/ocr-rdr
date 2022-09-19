import { useState } from "react";
import "./App.css";
import Placeholder from "./images/placeholder.png";

function App() {
  const [currentImage, setCurrentImage] = useState(1);

  return (
    <div className="container">
      <div className="image-container">
        <img
          src={`https://rdr.witteh.me/images/${currentImage}.png`}
          onError={(e: any) => (e.target.src = Placeholder)}
        />
      </div>

      <div className="controls-container">
        <div>
          <h1>Current ID: {currentImage}</h1>
        </div>
        <div>
          <button onClick={() => setCurrentImage(currentImage - 1)}>
            Previous Image
          </button>
          <button onClick={() => setCurrentImage(currentImage + 1)}>
            Next Image
          </button>
        </div>
        <div>
          <input
            onChange={(e: any) => {
              const newValue = parseInt(e.target.value);
              setCurrentImage(isNaN(newValue) ? 0 : newValue);
            }}
            placeholder="Enter id to skip to"
          />
        </div>
      </div>
    </div>
  );
}

export default App;
