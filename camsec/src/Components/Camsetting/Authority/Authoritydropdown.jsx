import { useState } from "react";
function Authoritydropdown({ selected, setSelected }) {
  const [isActive, setIsActive] = useState(false);
  const options = ["Admin", "Super Admin"];
  return (
    <div className="dropdown">
      <div className="dropdown-btn" data-toggle="dropdown"  onClick={(e) => setIsActive(!isActive)}>
        {selected}
        <span className="fas fa-caret-down caret"></span>
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
export default Authoritydropdown;
