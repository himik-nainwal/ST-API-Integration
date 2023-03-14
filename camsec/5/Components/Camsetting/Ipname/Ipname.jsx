import React from "react";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";
// import { Form } from "react";

const Ipname = () => {
  return (
    <div className="cam-selc-card">
      <MDBCard className="cam-selc-card">
        <MDBCardBody>
          <MDBCardTitle>I.P. Name</MDBCardTitle>
          <form >
            <label>
              
              <input type="text" />
            </label>
            {/* <input type="submit" value="Submit" /> */}
          </form>
        </MDBCardBody>
      </MDBCard>
    </div>
  );
};

export default Ipname;
