import React, { useState } from "react";
import Modal from 'react-modal';
import Webcam from "react-webcam";
// import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Container from "@material-ui/core/Container";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

import SignatureCanvas from "react-signature-canvas";
import ReactLoading from "react-loading";

import Message from "../Message";
import Header from "../Header";

import { PostFacialAPI } from "../api";

// const useStyle = makeStyles(theme => ({
//   cam: {
//     border: "1px solid red"
//   }
// }));

const customStyles = {
  content : {
    top                   : '50%',
    left                  : '50%',
    right                 : 'auto',
    bottom                : 'auto',
    marginRight           : '-50%',
    transform             : 'translate(-50%, -50%)'
  }
};

function Facial() {
  const [count, setCount] = useState(1);

  const [state, setState] = useState("success");

  const [message, setMessage] = useState("");

  const [showMessage, setShowMessage] = useState(false);

  const [loading, setLoading] = useState(false);

  const [mode, setMode] = useState("img");

  //   const classes = useStyle();
  const webcamRef = React.useRef(null);
  //   const capture = React.useCallback(() => {
  //     const imageSrc = webcamRef.current.getScreenshot();
  //   }, [webcamRef]);

  const pad = React.useRef(null);
  const getPad = React.useCallback(() => {
    const src = pad.current.toDataURL();
    pad.current.clear();
    console.log(src);
  }, [pad]);

  const [modalIsOpen, setModal] = useState(false);

  const [modalItem, setModalItem] = useState(["a","b","c"]);

  const [matric, setMatric] = useState("");

  return (
    <React.Fragment>
      <Header />

      {/*<button onClick={() => {setModal(true)}}>Open Modal</button>*/}
      <Modal
        isOpen={modalIsOpen}
        onRequestClose={() => {setModal(false)}}
        style={customStyles}
        contentLabel="Example Modal"
      >

        <h2>Select Your Matriculation Number</h2>
        {modalItem.map((item)=>(
            <div key = {item} style={{margin:10}}>
            <Button
              color="primary"
              variant="contained"
              disabled={loading}
              onClick={() => {
                setModal(false);
                console.log(count,item);
                PostFacialAPI({ count: count, matric: item })
                    .then(res => {
                      setTimeout(() => {
                        setState(res.state);
                        setMessage(res.message);
                        setMatric(res.matric);
                        setCount(6);
                        setMode(res.mode);
                        setShowMessage(true);
                        setLoading(false);
                      }, 1000);
                    })
                    .catch(err => {
                      console.log(err);
                    });
              }}
              fullWidth
            >
              {item}
            </Button>
            </div>
          ))
        }
        
      </Modal>

      <Container maxWidth="sm">
        <Grid
          container
          spacing={2}
          alignContent="center"
          alignItems="center"
          justify="center"
        >
          <Grid item xs={12}>
            <Typography>
              Place your face in the center of the frame.{" "}
            </Typography>
            <Typography>Click Take when ready. </Typography>
          </Grid>
          {loading && (
            <Grid item xs={2}>
              <ReactLoading type="spinningBubbles" color="#3f51b5" />
            </Grid>
          )}
          <Grid item xs={12}>
            {!loading && (
              <Message
                variant={state}
                message={message}
                open={showMessage}
                onClose={() => setShowMessage(false)}
              />
            )}
          </Grid>
          {mode === "img" ? (
            <Paper>
              {!loading && (
                <Grid item xs={12}>
                  <Webcam
                    audio={false}
                    ref={webcamRef}
                    screenshotFormat="image/jpeg"
                    width={530}
                  />
                </Grid>
              )}
            </Paper>
          ) : (
            <Paper>
              {!loading && (
                <Grid item xs={12}>
                  <SignatureCanvas
                    ref={pad}
                    canvasProps={{
                      width: 530,
                      height: 268,
                      className: "sigCanvas"
                    }}
                  />
                </Grid>
              )}
            </Paper>
          )}
          <Grid item xs={6}>
            {/* <Button color="primary" variant="contained" onClick={capture}>
          Take
        </Button> */}
            <Button
              color="primary"
              variant="contained"
              disabled={loading}
              onClick={() => {
                setLoading(true);
                
                if (mode === "img") {
                  const imageSrc = webcamRef.current.getScreenshot();
                  PostFacialAPI({ count: count, image:imageSrc })
                    .then(res => {
                      setTimeout(() => {
                        setState(res.state);
                        setMessage(res.message);
                        if (res.state === "success" && res.info === "lt5"){
                          setCount(1);
                        } else if (res.state === "warning" && res.info === "lt5"){
                          console.log(res.students);
                          setModalItem(res.students);
                          setModal(true);
                          setCount(5);
                        } else if (res.state === "success" && res.info === "lt6"){
                          setMatric(res.matric);
                          setCount(6);
                        } else if (res.state === "warning" && res.info === "lt6"){
                          setModalItem(res.students);
                          setModal(true);
                          setCount(5);
                        } else if (res.state === "error" && (res.info === "error-count" || res.info === "error-image" || res.info === "error-matric")){
                          setCount(1);
                        } else {
                          if (count < 4){
                            setCount(count+1);
                          } else {
                            setCount(count);
                          }
                          
                        }
                        setMode(res.mode);
                        setShowMessage(true);
                        setLoading(false);
                      }, 1000);
                    })
                    .catch(err => {
                      console.log(err);
                    });
                } else {
                  // getPad();
                  const imageSrc = pad.current.toDataURL();
                  pad.current.clear();
                  PostFacialAPI({ count: count, matric: matric, image:imageSrc })
                    .then(res => {
                      setTimeout(() => {
                        setState(res.state);
                        setMessage(res.message);
                        setMatric("");
                        setCount(1);
                        setMode(res.mode);
                        setShowMessage(true);
                        setLoading(false);
                      }, 1000);
                    })
                    .catch(err => {
                      console.log(err);
                    });
                }
                
                
                
              }}
              fullWidth
            >
              {mode === "img" ? "Take" : "Sign"}
            </Button>
          </Grid>
        </Grid>
      </Container>
    </React.Fragment>
  );
}

export default Facial;
