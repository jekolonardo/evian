import React from "react";
import { connect } from "react-redux";
import MaterialTable from "material-table";
import { forwardRef } from "react";
import AddBox from "@material-ui/icons/AddBox";
import ArrowUpward from "@material-ui/icons/ArrowUpward";
import Check from "@material-ui/icons/Check";
import ChevronLeft from "@material-ui/icons/ChevronLeft";
import ChevronRight from "@material-ui/icons/ChevronRight";
import Clear from "@material-ui/icons/Clear";
import DeleteOutline from "@material-ui/icons/DeleteOutline";
import Edit from "@material-ui/icons/Edit";
import FilterList from "@material-ui/icons/FilterList";
import FirstPage from "@material-ui/icons/FirstPage";
import LastPage from "@material-ui/icons/LastPage";
import Remove from "@material-ui/icons/Remove";
import SaveAlt from "@material-ui/icons/SaveAlt";
import Search from "@material-ui/icons/Search";
import ViewColumn from "@material-ui/icons/ViewColumn";

import Dialog from "@material-ui/core/Dialog";
import { actionCreators } from "./store";

function SessionAttendance(props) {
  const tableIcons = {
    Add: forwardRef((props, ref) => <AddBox {...props} ref={ref} />),
    Check: forwardRef((props, ref) => <Check {...props} ref={ref} />),
    Clear: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Delete: forwardRef((props, ref) => <DeleteOutline {...props} ref={ref} />),
    DetailPanel: forwardRef((props, ref) => (
      <ChevronRight {...props} ref={ref} />
    )),
    Edit: forwardRef((props, ref) => <Edit {...props} ref={ref} />),
    Export: forwardRef((props, ref) => <SaveAlt {...props} ref={ref} />),
    Filter: forwardRef((props, ref) => <FilterList {...props} ref={ref} />),
    FirstPage: forwardRef((props, ref) => <FirstPage {...props} ref={ref} />),
    LastPage: forwardRef((props, ref) => <LastPage {...props} ref={ref} />),
    NextPage: forwardRef((props, ref) => <ChevronRight {...props} ref={ref} />),
    PreviousPage: forwardRef((props, ref) => (
      <ChevronLeft {...props} ref={ref} />
    )),
    ResetSearch: forwardRef((props, ref) => <Clear {...props} ref={ref} />),
    Search: forwardRef((props, ref) => <Search {...props} ref={ref} />),
    SortArrow: forwardRef((props, ref) => <ArrowUpward {...props} ref={ref} />),
    ThirdStateCheck: forwardRef((props, ref) => (
      <Remove {...props} ref={ref} />
    )),
    ViewColumn: forwardRef((props, ref) => <ViewColumn {...props} ref={ref} />)
  };

  // vars from store
  const { sessionAttendance, openSession, tableTitle } = props;

  // methods from store
  const { handleInputUpdate, overwriteStatus } = props;

  const columns = [
    {
      title: "Name",
      field: "name",
      editable: "never"
    },
    { title: "Matric", field: "matric", editable: "never" },
    {
      title: "Status",
      field: "status",
      lookup: { absent: "absent", present: "present", mc: "mc" }
    },
    {
      title: "Signature",
      field: "signature",
      editable: "never",
      render: rowData => (rowData.signature)?<img src={"data:image/jpg;base64,"+rowData.signature} style={{height: 100}}/>:<p>-</p>
    }
  ];

  return (
    <React.Fragment>
      <Dialog
        open={openSession}
        onClose={() => handleInputUpdate("openSession", false)}
        fullWidth
        maxWidth={false}
      >
        <MaterialTable
          icons={tableIcons}
          options={{
            pageSize: 10
          }}
          title={tableTitle}
          columns={columns}
          data={sessionAttendance}
          editable={{
            onRowUpdate: (newData, oldData) =>
              new Promise(resolve => {
                overwriteStatus(newData);
                setTimeout(() => {
                  resolve();
                  const data = [...sessionAttendance];
                  data[data.indexOf(oldData)] = newData;
                  //   setState({ ...sessionAttendance, data });
                  handleInputUpdate("sessionAttendance", data);
                }, 600);
              })
          }}
        />
      </Dialog>
    </React.Fragment>
  );
}

const mapStateToProps = state => {
  return {
    sessionAttendance: state.PagesReducer.sessionAttendance,
    openSession: state.PagesReducer.openSession,
    tableTitle: state.PagesReducer.tableTitle
  };
};

const mapDispatchToProps = dispatch => ({
  handleInputUpdate: (name, value) => {
    dispatch(actionCreators.handleInputUpdate(name, value));
  },
  overwriteStatus: data => {
    dispatch(actionCreators.overwriteStatus(data));
  }
});

export default connect(
  mapStateToProps,
  mapDispatchToProps
)(SessionAttendance);
