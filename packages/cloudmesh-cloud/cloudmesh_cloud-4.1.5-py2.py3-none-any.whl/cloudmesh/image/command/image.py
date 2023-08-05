from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.variables import Variables
from cloudmesh.compute.vm.Provider import Provider
from cloudmesh.management.configuration.arguments import Arguments
from cloudmesh.mongo.CmDatabase import CmDatabase
from cloudmesh.shell.command import PluginCommand
from cloudmesh.shell.command import command, map_parameters
from cloudmesh.common.parameter import Parameter

class ImageCommand(PluginCommand):

    # see https://github.com/cloudmesh/client/blob/master/cloudmesh_client/shell/plugins/ImageCommand.py

    # noinspection PyUnusedLocal
    @command
    def do_image(self, args, arguments):
        """
        ::

            Usage:
                image list [NAMES] [--cloud=CLOUD] [--refresh] [--output=OUTPUT] [--query=QUERY]

            Options:
               --output=OUTPUT  the output format [default: table]
               --cloud=CLOUD    the cloud name
               --refresh        live data taken from the cloud

            Description:
                image list
                image list --cloud=aws --refresh
                image list --output=csv
                image list 58c9552c-8d93-42c0-9dea-5f48d90a3188 --refresh
        """

        map_parameters(arguments,
                       "refresh",
                       "cloud",
                       "output")

        variables = Variables()

        arguments.output = Parameter.find("output",
                                          arguments,
                                          variables,
                                          "table")

        arguments.refresh = Parameter.find_bool("refresh",
                                                arguments,
                                                variables)
        if arguments.list and arguments["--query"]:
            names = []

            clouds, names = Arguments.get_cloud_and_names("list",
                                                          arguments,
                                                          variables)
            cloud = clouds[0]
            query = arguments["--query"]

            provider = Provider(name=cloud)

            images = []
            #
            # images = provider.images(query=query)
            #

            return NotImplementedError

            provider.Print(arguments.output, images)

            return ""

        if arguments.list and arguments.refresh:

            names = []

            clouds, names = Arguments.get_cloud_and_names("list",
                                                          arguments,
                                                          variables)

            for cloud in clouds:
                print(f"cloud {cloud}")
                provider = Provider(name=cloud)
                images = provider.images()

                provider.Print(images, output=arguments.output, kind="image")

            return ""

        elif arguments.list:

            names = []

            clouds, names = Arguments.get_cloud_and_names("list",
                                                          arguments,
                                                          variables)

            print(clouds, names)
            print("find images")
            try:

                for cloud in clouds:
                    print(f"List {cloud}")
                    provider = Provider(name=cloud)

                    db = CmDatabase()


                    # print(images)
                    # print(provider)
                    if len(names) == 0 :
                        images = db.find(collection=f"{cloud}-image")
                        provider.Print(images, output=arguments.output,
                                   kind="image")
                    else:
                        images = []
                        for name in names:
                            images += db.find_name(name,kind='image')
                        provider.Print(images, output=arguments.output,
                                       kind="image")

            except Exception as e:

                VERBOSE(e)

            return ""
