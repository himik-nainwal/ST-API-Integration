import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Assigndropdown from "./Assigndropdown";

import { useState } from "react";

const Assign = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selc-card" >
      <MDBCard className='cam-selc-card ' >
        <MDBCardBody className="card-body">
          <MDBCardTitle >Assign</MDBCardTitle>

          <Assigndropdown selected={selected} setSelected={setSelected} />  
          
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Assign;
