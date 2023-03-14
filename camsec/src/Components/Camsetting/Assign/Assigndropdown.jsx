import { useState } from "react";
function Assigndropdown({ selected, setSelected, value2 }) {
  const [isActive, setIsActive] = useState(false);
  console.log("hhhhhhhhh",value2)
  const options = ["FaceMetric Sec", "Emergency Sec", "Monotoring Sec"];
  return (
    <div className="dropdown">
      <div className="dropdown-btn" onClick={(e) => setIsActive(!isActive)}>
        {selected}
        <span className="fas fa-caret-down"></span>
      </div>
      {isActive && (
        <div className="dropdown-content">
          {options.map((option) => (
            <div
              onClick={(e) => {
                setSelected(option);
                setIsActive(false);
              }}
              className="dropdown-item"
            >
              {option}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Assigndropdown;
