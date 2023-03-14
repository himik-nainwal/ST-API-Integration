import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Pointsdropdown from "./Pointsdropdown";

import { useState } from "react";

const Points = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selc-card" >
      <MDBCard className='cam-selc-card' >
        <MDBCardBody>
          <MDBCardTitle>Assign</MDBCardTitle>

          <Pointsdropdown selected={selected} setSelected={setSelected} />  
          
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Points;
