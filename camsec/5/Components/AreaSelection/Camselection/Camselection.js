import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
import Camsdropdown from "./Camsdropdown";

import { useState } from "react";

const Assign = () => {
  const [selected, setSelected] = useState("Choose One");

  return (
    <div className="cam-selccard" >
      <MDBCard className='cam-selccard card' >
        <MDBCardBody>
          <MDBCardTitle>Assign</MDBCardTitle>

          <Camsdropdown selected={selected} setSelected={setSelected} />  
          
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Assign;
