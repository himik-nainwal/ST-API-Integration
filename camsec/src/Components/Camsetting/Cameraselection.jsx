import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
// import {
//   MDBDropdown,
//   MDBDropdownMenu,
//   MDBDropdownToggle,
//   MDBDropdownItem,
//   MDBDropdownLink,
// } from "mdb-react-ui-kit";
import Dropdown from "../Dropdown";
import { useState } from "react";

const Camselection = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selc-card" >
      <MDBCard className='cam-selc-card' >
        <MDBCardBody>
          <MDBCardTitle>Camera Selection</MDBCardTitle>
          <Dropdown selected={selected} setSelected={setSelected} />      
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Camselection;
