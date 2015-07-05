from galaxy.util import bunch
from galaxy import model


class MockTrans( object ):

    def __init__( self ):
        self.app = TestApp()


class TestApp( object ):

    def __init__( self ):
        self.config = bunch.Bunch(
            tool_secret="awesome_secret",
        )
        self.model = model.mapping.init(
            "/tmp",
            "sqlite:///:memory:",
            create_tables=True
        )
        self.toolbox = TestToolbox()
        self.datatypes_registry = TestDatatypesRegistry()


class TestDatatypesRegistry( object ):

    def __init__( self ):
        pass

    def get_datatype_by_extension( self, ext ):
        return ext


class TestToolbox( object ):

    def __init__( self ):
        self.tools = {}

    def get_tool( self, tool_id, tool_version=None ):
        # Real tool box returns None of missing tool also
        return self.tools.get( tool_id, None )

    def get_tool_id( self, tool_id ):
        tool = self.get_tool( tool_id )
        return tool and tool.id

class TestWorkflow( object ):

    def __init__( self ):
        self.workflow = model.Workflow()

    def add_step( self, type,order_index=0,
                 tool_inputs={"name": "input1"},
                 input_connections=[],
                 position={"top": 1, "left": 1},
                 **kwargs ):

        workflow_step = model.WorkflowStep()
        workflow_step.type=type
        workflow_step.order_index=order_index
        workflow_step.tool_inputs=tool_inputs
        workflow_step.input_connections=input_connections
        workflow_step.position=position
        for key, value in kwargs.iteritems():
            setattr(workflow_step, key, value)
        self.workflow.steps.append( workflow_step )
        return workflow_step

    @classmethod
    def build_connection(Class, input_name, output_step, output_name, **kwargs ):
        conn = model.WorkflowStepConnection()
        conn.input_name = input_name
        conn.output_step = output_step
        conn.output_name = output_name
        for key, value in kwargs.iteritems():
            setattr(conn, key, value)
        return conn

